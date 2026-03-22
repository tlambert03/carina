# Qlementine Theme Generation via Radix Color System

## Overview

Generate a complete Qlementine theme JSON from 3 color inputs + a light/dark toggle,
using the Radix color generation algorithm as the engine. The user-facing interface is
identical to the Radix playground at radix-ui.com/colors/custom.

**Inputs:** `accent_hex`, `gray_hex`, `background_hex`, `appearance: light | dark`  
**Output:** A valid Qlementine theme JSON file

---

## Architecture: 3 Modules

### `radix_generator.py` (~200 lines)
Direct Python port of the JS `generateRadixColors` function from the
`radix-ui/website` repo (`components/generateRadixColors.tsx`). No Qlementine
awareness. Takes `(accent, gray, background, appearance)`, returns the same data
structure as the JS original.

**Dependencies:**
- `coloraide` — replaces `colorjs.io` (same OKLCh math, deltaEOK, APCA)
- `@radix-ui/colors` P3 data — vendored once as JSON (dump from npm package)
- Bezier easing — ~15 lines inlined (replaces `bezier-easing` npm package)

**Output structure:**
```python
{
    "accentScale":              list[str],  # 12 sRGB hex values
    "accentScaleAlpha":         list[str],  # 12 alpha hex values
    "accentScaleWideGamut":     list[str],  # 12 oklch strings
    "accentScaleAlphaWideGamut":list[str],
    "accentContrast":           str,        # APCA-computed text color on step 9
    "grayScale":                list[str],  # 12 sRGB hex values
    "grayScaleAlpha":           list[str],
    "grayScaleWideGamut":       list[str],
    "grayScaleAlphaWideGamut":  list[str],
    "background":               str,
}
```

### `qlementine_mapper.py` (~180 lines)
Consumes generator output and produces the Qlementine JSON dict.
Calls the generator **5 times total**: once for the user's accent,
then four more with fixed seeds for the status color groups.

### `app.py`
UI wrapper — Qt dialog, CLI, or web interface. Just calls the other two.

---

## How the Radix Algorithm Works (summary)

Given an accent color input:

1. **Find closest named Radix scale** — converts input to OKLCh, computes deltaEOK
   against all 29 hand-crafted named scales, picks the two closest and blends them
   using trigonometric interpolation (ratio of tangents of the triangle formed by
   the three distances).

2. **Adjust hue and chroma** — sets every step's hue to the input hue, scales
   chroma proportionally, caps at 1.5× input chroma.

3. **Transpose lightness progression to match background** — the pre-built scales
   assume a standard background. If your background differs, the whole lightness ramp
   is remapped via a Bezier easing curve so step 1 starts from your actual background
   lightness. Light mode easing: `[0, 2, 0, 2]`. Dark mode: `[1, 0, 1, 0]`.

4. **Step 9 is the exact input color** (if perceptually distinct from background).
   Step 10 (hover) is computed by nudging L up or down depending on lightness.

5. **Alpha variants** — back-solves the alpha value that produces each solid color
   when composited over the given background. Background-dependent.

6. **Accent contrast** — APCA check: white if contrast ≥ Lc 40, otherwise a dark
   hue-matched color.

---

## Hover/Press Convention

Qlementine **always lightens** on hover and press, in both light and dark mode.
Radix step 10 darkens in light mode and lightens in dark mode — a conflict in
light mode.

Resolution: derive hover/press colors by nudging OKLCh `L` directly from the
base step, using the following calibrated ΔL constants (measured from both
reference themes):

| Color group | Mode | Hover ΔL | Pressed ΔL | Direction |
|---|---|---|---|---|
| primary / primaryAlt | both | +0.035 | +0.070 | lighten |
| neutral | light | +0.006 | +0.012 | lighten (subtle) |
| neutral | dark | +0.034 | +0.070 | lighten |
| border | light | −0.100 | −0.150 | **darken** (unusual) |
| border | dark | +0.052 | +0.138 | lighten |
| secondaryAlt (muted text) | light | −0.094 | −0.047 | darken |
| secondaryAlt (muted text) | dark | +0.114 | +0.170 | lighten |

Note: border and secondaryAlt hover/press are better read directly from
gray scale steps rather than derived — see mapping table below.

---

## Complete Mapping Table

Indices are 0-based: `accent[8]` = step 9, `accent[11]` = step 12.

### Accent Scale → `primary*` fields

| Qlementine field | Source | Notes |
|---|---|---|
| `primaryColor` | `accent[8]` | Exact brand color — step 9 by Radix design |
| `primaryColorHovered` | `accent[8]` + ΔL +0.035 | Derive; Radix step 10 goes wrong direction in light |
| `primaryColorPressed` | `accent[8]` + ΔL +0.070 | Derive |
| `primaryColorDisabled` | `accent[3]` | Step 4 — pale tinted background |
| `primaryColorTransparent` | `primaryColor` @ alpha=0 | Auto-derived by Qlementine from JSON |
| `primaryColorForeground` | `accentContrast` | APCA-computed white or dark |
| `primaryColorForegroundHovered` | same as `primaryColorForeground` | Always identical |
| `primaryColorForegroundPressed` | same as `primaryColorForeground` | Always identical |
| `primaryColorForegroundDisabled` | `accent[3]` tinted | Light: pale tint of step 4; Dark: `gray[6]` |
| `primaryAlternativeColor` | `accent[10]` (light) / `accent[7]` (dark) | Always visually darker than `primaryColor`; see note |
| `primaryAlternativeColorHovered` | `accent[9]` | Step 10 |
| `primaryAlternativeColorPressed` | `accent[8]` | Step 9, same as primary base |
| `primaryAlternativeColorDisabled` | `accent[5]` (light) / `accent[3]` (dark) | Step 6 / step 4 |
| `primaryAlternativeColorTransparent` | `primaryAlternativeColor` @ alpha=0 | Auto-derived |
| `focusColor` | `accent[8]` @ 40% alpha | Step 9 with transparency |

**Note on `primaryAlternativeColor`:**
The invariant is that it is always *visually darker* than `primaryColor` (used for
selected+checked fill states). In light mode this means step 11 (L≈0.558 < 0.649);
in dark mode step 8 (L≈0.543 < 0.655). The step differs between modes because the
Radix dark scale inverts the lightness ordering relative to light.

### Gray Scale → `background*`, `neutral*`, `border*`, `secondary*` fields

| Qlementine field | Source | Notes |
|---|---|---|
| `backgroundColorMain1` | `gray[0]` | Step 1, ≈ background input |
| `backgroundColorMain2` | `gray[2]` | Step 3, **not step 2** — scale is transposed to background |
| `backgroundColorMain3` | `gray[4]` | Step 5 |
| `backgroundColorMain4` | `gray[4]` | Step 5, same as Main3 |
| `backgroundColorMainTransparent` | `gray[0]` @ alpha=0 | Auto-derived |
| `backgroundColorWorkspace` | `gray[7]` | Step 8 — significantly darker |
| `backgroundColorTabBar` | `gray[4]` (light) / `gray[0]` (dark) | Step 5 light, step 1 dark |
| `neutralColorDisabled` | `gray[2]` | Step 3 |
| `neutralColor` | `gray[6]` | Step 7 |
| `neutralColorHovered` | `gray[6]` + ΔL | Derive: +0.006 light / +0.034 dark |
| `neutralColorPressed` | `gray[6]` + 2ΔL | Derive: +0.012 light / +0.070 dark |
| `neutralColorTransparent` | `neutralColor` @ alpha=0 | Auto-derived |
| `borderColorDisabled` | `gray[3]` | Step 4 |
| `borderColor` | `gray[6]` | Step 7, same step as `neutralColor` |
| `borderColorHovered` | `gray[7]` (light) / `gray[6]`+ΔL (dark) | Light darkens; dark lightens |
| `borderColorPressed` | `gray[8]` (light) / `gray[6]`+2ΔL (dark) | Light darkens; dark lightens |
| `borderColorTransparent` | `borderColor` @ alpha=0 | Auto-derived |
| `secondaryColorDisabled` | `gray[5]` (light) / `#ffffff` @ 20% alpha (dark) | Different strategies per mode |
| `secondaryAlternativeColorDisabled` | `gray[3]` (light) / `grayAlpha[8]` (dark) | Step 4 light |
| `secondaryAlternativeColor` | `gray[8]` | Step 9 — muted/placeholder text |
| `secondaryAlternativeColorHovered` | `gray[9]` (light inverted) / `gray[9]` (dark) | Step 10 |
| `secondaryAlternativeColorPressed` | `gray[9]` | Step 10 |
| `secondaryAlternativeColorTransparent` | `secondaryAlternativeColor` @ alpha=0 | Auto-derived |
| `secondaryColor` | APCA derive (light) / `#ffffff` (dark) | See note |
| `secondaryColorHovered` | `secondaryColor` − ΔL (light) / `gray[11]` (dark) | |
| `secondaryColorPressed` | `secondaryColor` − 2ΔL (light) / `gray[11]` (dark) | |
| `secondaryColorDisabled` | `gray[5]` (light) / `#ffffff` @ 20% alpha (dark) | |
| `secondaryColorTransparent` | `secondaryColor` @ alpha=0 | Auto-derived |
| `secondaryColorForeground` | `#ffffff` (light) / `gray[2]` (dark) | Text on dark tooltip surfaces |
| `secondaryColorForegroundHovered` | same as `secondaryColorForeground` | |
| `secondaryColorForegroundPressed` | same as `secondaryColorForeground` | |
| `secondaryColorForegroundDisabled` | `gray[2]` (subtle) | |

**Note on `secondaryColor` (main text):**
The light theme text color (L≈0.37) falls in a gap between Radix gray steps 11
(L≈0.503) and 12 (L≈0.247) — no step lands there. Derive it via APCA: find the
OKLCh L value that achieves ~Lc 75 contrast against the background, with near-zero
chroma matched to the gray hue. This is the same technique Radix uses internally
for `accentContrast`.

In dark mode, `secondaryColor` is always pure white (`#ffffff`). No derivation needed.

### Hardcoded Values

These are not derived from the scales.

**Light mode:**
| Field | Value |
|---|---|
| `semiTransparentColor1` | `rgba(0, 0, 0, 4%)` = `#0000000a` |
| `semiTransparentColor2` | `rgba(0, 0, 0, 10%)` = `#00000019` |
| `semiTransparentColor3` | `rgba(0, 0, 0, 13%)` = `#00000021` |
| `semiTransparentColor4` | `rgba(0, 0, 0, 16%)` = `#00000028` |
| `shadowColor1` | `rgba(0, 0, 0, 12%)` = `#00000020` |
| `shadowColor2` | `rgba(0, 0, 0, 25%)` = `#00000040` |
| `shadowColor3` | `rgba(0, 0, 0, 38%)` = `#00000060` |

**Dark mode:**
| Field | Value |
|---|---|
| `semiTransparentColor1` | `accent[11]` @ 9% alpha |
| `semiTransparentColor2` | `accent[11]` @ 14% alpha |
| `semiTransparentColor3` | `accent[11]` @ 16% alpha |
| `semiTransparentColor4` | `accent[11]` @ 18% alpha |
| `shadowColor1` | `rgba(0, 0, 0, 40%)` = `#00000066` |
| `shadowColor2` | `rgba(0, 0, 0, 73%)` = `#000000bb` |
| `shadowColor3` | `rgba(0, 0, 0, 100%)` = `#000000ff` |

Dark mode `semiTransparentColor` uses the lightest accent step (step 12) as the
tint base rather than pure black. This is consistent with how Qlementine's official
dark theme works — pure black overlays look wrong on blue-tinted dark surfaces.

### Status Colors

Run `generateRadixColors()` four additional times with fixed accent seed colors,
passing the user's `gray` and `background` inputs unchanged so the disabled states
harmonize with the overall background.

**Seeds:**
| Status | Seed hex | OKLCh hue |
|---|---|---|
| success | `#2bb5a0` | H ≈ 180° (teal) |
| info | `#1ba8d5` | H ≈ 227° (cyan) |
| warning | `#fbc064` | H ≈ 77° (amber) |
| error | `#e96b72` | H ≈ 19° (red) |

**Mapping (same for all four):**
| Qlementine field | Source |
|---|---|
| `statusColorX` | `x_scale[8]` — step 9, solid |
| `statusColorXHovered` | `x_scale[9]` — step 10 |
| `statusColorXPressed` | `x_scale[10]` — step 11 |
| `statusColorXDisabled` | `x_scale[3]` — step 4 (light: pale tint; dark: bg-tinted) |
| `statusColorForeground` | `#ffffff` always |
| `statusColorForegroundHovered` | `#ffffff` always |
| `statusColorForegroundPressed` | `#ffffff` always |
| `statusColorForegroundDisabled` | `#ffffff` @ 60% alpha |

Note: if the user's accent color is close in hue to one of the status seeds (e.g.
a red accent), the error status color will be nearly identical to the accent. Worth
detecting and warning, or offering a hue-shifted fallback.

---

## Dark Mode Special Cases

These fields behave differently enough in dark mode to warrant explicit callout:

| Field | Dark mode value | Reason |
|---|---|---|
| `secondaryColor` | `#ffffff` | Text on dark bg is always white |
| `secondaryColorDisabled` | `#ffffff` @ 20% alpha | Muted white, not gray |
| `secondaryColorForeground` | `backgroundColorMain2` | Text on tooltip/dark surfaces reverses to bg color |
| `semiTransparentColor[1-4]` | `accent[11]` at low alpha | Tinted overlay, not pure black |
| `shadowColor[1-3]` | Stronger blacks (40/73/100%) | Dark themes need heavier shadows |
| `backgroundColorTabBar` | `gray[0]` (= main1) | In dark, tab bar ≈ main background |
| `primaryColorForegroundDisabled` | `gray[6]` | Muted blue-tinted gray, not pale tint |

---

## Confidence Assessment

| Color group | Confidence | Notes |
|---|---|---|
| Primary / accent | High | Steps validated against both themes to ΔL < 0.02 |
| Background steps | High | Very clean match, both modes |
| Neutral | High | Step assignments confirmed; ΔL constants calibrated |
| Border | High | Confirmed; note direction flip in light mode |
| Secondary text | High | Dark = white; light = APCA derive, both confirmed |
| Status colors | Medium-high | Seeds produce correct solid colors; disabled states in dark may need visual tuning |
| semiTransparent dark | Medium | Tint formula inferred from one dark theme; correct in principle, may want visual tuning |

---

## Fields Not Derived From Color Scales

The following fields from `Theme.hpp` are metric/typography values and are
unrelated to the color generation system. Expose them separately as direct
user inputs with sensible defaults:

```
fontSize, fontSizeMonospace, fontSizeH1-H5, fontSizeS1
animationDuration, focusAnimationDuration, sliderAnimationDuration
borderRadius, checkBoxBorderRadius, menuItemBorderRadius, menuBarItemBorderRadius
borderWidth, focusBorderWidth
controlHeightLarge/Medium/Small, controlDefaultWidth
spacing
scrollBarThicknessFull/Small, scrollBarMargin
tabBarPaddingTop, tabBarTabMaxWidth/MinWidth
sliderGrooveHeight, sliderTickSize/Spacing/Thickness
progressBarGrooveHeight
dialMarkLength/Thickness, dialTickLength/Spacing, dialGrooveThickness
iconSize, iconSizeMedium/Large/ExtraSmall
useSystemFonts
```

These can be exposed as a second panel ("Metrics") in the UI, or left at
Qlementine defaults and omitted from the JSON (Qlementine will use its compiled-in
defaults for any missing fields).

---

## Fields Defined in `Theme.hpp` but Unused in `QlementineStyle.cpp`

These are defined but never referenced in the style engine. Safe to omit from
generated JSON or set to the default values — Qlementine won't use them:

```
backgroundColorMain4
backgroundColorWorkspace
primaryAlternativeColorHovered
primaryAlternativeColorPressed
primaryColorForegroundTransparent
secondaryAlternativeColorTransparent
secondaryColorForegroundHovered
secondaryColorForegroundPressed
secondaryColorForegroundTransparent
semiTransparentColor3
```
