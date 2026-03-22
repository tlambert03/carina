---
icon: lucide/citrus
---

# Qlementine Guide

!!!info "Purpose of this Guide"
    `carina` wraps [Qlementine](https://github.com/oclero/qlementine).  This guide
    serves as a developer reference for how the properties defined in Qlementine's
    `Theme` struct correspond to the visual elements of Qt widgets styled by
    Qlementine.

This guide provides a comprehensive reference for how each property in the
`Theme` struct (defined in `Theme.hpp`) maps to visual elements in Qlementine's
styled widgets. It is designed to answer two questions:

1. **Theme → Widget**: Given a theme property, which widgets are affected?
1. **Widget → Theme**: Given a Qt widget, which theme properties control its appearance?

---

## Theme Property → Widgets

### Colors

#### Background Colors

| <div style="min-width: 220px;">Theme Property</div>               | Affected Widgets / Visual Elements                                                                                          |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `backgroundColorMain1`            | QLineEdit/QTextEdit field fill, QCheckBox unchecked indicator, QMenu background, QComboBox (editable) background, QSpinBox field, item view Base palette     |
| `backgroundColorMain2`            | QMenuBar background, QToolBar background, QStatusBar background, selected QTab background, QGroupBox composite fill, Window palette color                   |
| `backgroundColorMain3`            | Pressed button backgrounds, disabled QLineEdit/QTextEdit field, QHeaderView cell background, QGroupBox composite, disabled QTabBar background               |
| `backgroundColorMain4`            | Reserved – not currently referenced in draw code                                                                                                            |
| `backgroundColorMainTransparent`  | Disabled QFrame/QGroupBox background, unselected QTab transparent fill                                                                                      |
| `backgroundColorWorkspace`        | Available for workspace backgrounds (set in palette, not directly in draw functions)                                                                        |
| `backgroundColorTabBar`           | QTabBar container background                                                                                                                                |

#### Neutral Colors

| <div style="min-width: 220px;">Theme Property</div>               | Affected Widgets / Visual Elements                                                                                                   |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `neutralColor`              | Default QPushButton background, QToolButton hover, QSlider groove, QDial background/handle, QProgressBar groove, QHeaderView hover, item view hover, QTab hover, switch track |
| `neutralColorHovered`       | Default QPushButton hover, QToolButton hover, QHeaderView pressed, tab close button pressed (selected tab)                           |
| `neutralColorPressed`       | Default QPushButton pressed, QToolButton pressed, QDial groove/ticks, item view pressed, cell focus border                           |
| `neutralColorDisabled`      | Disabled default QPushButton, QToolButton, QSlider groove, QDial, QProgressBar groove, item views, switch track                      |
| `neutralColorTransparent`   | QToolButton normal (flat), unselected QTab default, item view normal/transparent, cell focus border (unfocused)                      |

#### Focus Color

| <div style="min-width: 220px;">Theme Property</div>  | Affected Widgets / Visual Elements                                               |
| :------------- | :------------------------------------------------------------------------------- |
| `focusColor`   | Focus ring on all focusable widgets (QPushButton, QCheckBox, QComboBox, etc.)    |

#### Primary Colors

| <div style="min-width: 250px;">Theme Property</div>   | Affected Widgets / Visual Elements                                                                                                                    |
| :---------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `primaryColor`                      | Primary QPushButton bg, QCheckBox checked bg, QSlider value fill, QProgressBar value fill, QDial value arc, selected item bg, QMenu item hover, focused QLineEdit border, QSplitter hover, QMenuBar item hover |
| `primaryColorHovered`               | Hovered primary QPushButton, QSlider value, QSplitter pressed                                                                                        |
| `primaryColorPressed`               | Pressed primary QPushButton, QSlider value                                                                                                           |
| `primaryColorDisabled`              | Disabled primary QPushButton, QSlider/QProgressBar/QDial value, disabled selected items                                                              |
| `primaryColorTransparent`           | QMenu item normal (transparent), unselected item view transparent, cell focus unfocused                                                              |
| `primaryColorForeground`            | Text on primary QPushButton, QSlider handle, switch handle (checked), selected item text, QCheckBox checkmark, QMenu item text (on hover)            |
| `primaryColorForegroundHovered`     | Text on hovered primary QPushButton, QSlider handle, switch handle, QMenu item text hover                                                            |
| `primaryColorForegroundPressed`     | Text on pressed primary QPushButton, QSlider handle, switch handle                                                                                   |
| `primaryColorForegroundDisabled`    | Disabled text on primary QPushButton, disabled selected item text, disabled checkmark                                                                |
| `primaryColorForegroundTransparent` | Transparent text on primary backgrounds (animation endpoints)                                                                                        |

#### Primary Alternative Colors

| <div style="min-width: 250px;">Theme Property</div>  | Affected Widgets / Visual Elements                                                 |
| :-------------------------------------- | :--------------------------------------------------------------------------------- |
| `primaryAlternativeColor`               | Item view checkbox bg (checked, selected), list checkbox border (checked, not selected) |
| `primaryAlternativeColorHovered`        | Reserved – not directly used in current draw code                                  |
| `primaryAlternativeColorPressed`        | Reserved – not directly used in current draw code                                  |
| `primaryAlternativeColorDisabled`       | Disabled item view checkbox (checked, selected)                                    |
| `primaryAlternativeColorTransparent`    | Item view checkbox border (checked, selected, disabled)                            |

#### Secondary Colors

| <div style="min-width: 260px;">Theme Property</div>  | Affected Widgets / Visual Elements                                                                                                                                                        |
| :-------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `secondaryColor`                        | Primary text color: QLabel, QLineEdit text, QComboBox text, default QPushButton text, QMenu item text, QTab text, QDial needle, QToolTip background, switch handle (unchecked)            |
| `secondaryColorHovered`                 | Hovered text: default QPushButton, QComboBox, QToolButton separator, switch handle (unchecked), scrollbar base                                                                           |
| `secondaryColorPressed`                 | Pressed text: QToolButton separator, switch handle (unchecked), QToolTip border                                                                                                          |
| `secondaryColorDisabled`                | Disabled text: QLabel, QLineEdit, QComboBox, QPushButton, QMenu item, QToolBar/QStatusBar separators, QDial needle, switch handle, icons                                                |
| `secondaryColorTransparent`             | Invisible text: disabled QTab close button icon                                                                                                                                          |
| `secondaryColorForeground`              | Text on dark backgrounds: QToolTip text, secondary QPushButton text, QToolButton text, selected QMenu item text, item icon color                                                        |
| `secondaryColorForegroundHovered`       | Hovered text on dark backgrounds: secondary QPushButton, QMenu secondary text                                                                                                            |
| `secondaryColorForegroundPressed`       | Pressed text on dark backgrounds: secondary QPushButton, QMenu secondary text                                                                                                            |
| `secondaryColorForegroundDisabled`      | Disabled text on dark backgrounds: secondary QPushButton, QToolButton, disabled selected items, item icons                                                                               |
| `secondaryColorForegroundTransparent`   | Transparent secondary foreground text (animation endpoints)                                                                                                                              |

#### Secondary Alternative Colors

| <div style="min-width: 260px;">Theme Property</div>  | Affected Widgets / Visual Elements                                             |
| :----------------------------------------- | :----------------------------------------------------------------------------- |
| `secondaryAlternativeColor`                | Caption/description text: QLabel captions, item view captions, QLineEdit placeholder, QScrollBar handle normal, command button descriptions |
| `secondaryAlternativeColorHovered`         | QScrollBar handle hovered                                                      |
| `secondaryAlternativeColorPressed`         | QScrollBar handle pressed                                                      |
| `secondaryAlternativeColorDisabled`        | Disabled caption text, disabled command button descriptions                    |
| `secondaryAlternativeColorTransparent`     | Reserved – not directly used in current draw code                              |

#### Status Colors

| <div style="min-width: 250px;">Theme Property</div>  | Affected Widgets / Visual Elements                                             |
| :----------------------------- | :----------------------------------------------------------------------------- |
| `statusColorSuccess`           | QLineEdit/QComboBox border with Success status                                 |
| `statusColorSuccessHovered`    | Same as above when focused/hovered                                             |
| `statusColorSuccessPressed`    | Same as above when pressed                                                     |
| `statusColorSuccessDisabled`   | Same as above when disabled                                                    |
| `statusColorInfo`              | QLineEdit/QComboBox border with Info status                                    |
| `statusColorInfoHovered`       | Same as above when focused/hovered                                             |
| `statusColorInfoPressed`       | Same as above when pressed                                                     |
| `statusColorInfoDisabled`      | Same as above when disabled                                                    |
| `statusColorWarning`           | QLineEdit/QComboBox border and text with Warning status                        |
| `statusColorWarningHovered`    | Same as above when focused/hovered                                             |
| `statusColorWarningPressed`    | Same as above when pressed                                                     |
| `statusColorWarningDisabled`   | Same as above when disabled                                                    |
| `statusColorError`             | QLineEdit/QComboBox border and text with Error status                          |
| `statusColorErrorHovered`      | Same as above when focused/hovered                                             |
| `statusColorErrorPressed`      | Same as above when pressed                                                     |
| `statusColorErrorDisabled`     | Same as above when disabled                                                    |
| `statusColorForeground`        | Text on status-colored backgrounds (normal)                                    |
| `statusColorForegroundHovered` | Same as above when hovered                                                     |
| `statusColorForegroundPressed` | Same as above when pressed                                                     |
| `statusColorForegroundDisabled`| Same as above when disabled                                                    |

#### Shadow Colors

| Theme Property           | Affected Widgets / Visual Elements                                    |
| :----------------------- | :-------------------------------------------------------------------- |
| `shadowColor1`           | QMenu drop shadow, QTabBar top/bottom shadows, QHeaderView shadow     |
| `shadowColor2`           | QTab separator shadow                                                 |
| `shadowColor3`           | QSlider handle shadow, QDial handle shadow                            |
| `shadowColorTransparent` | Shadow gradient endpoints (fade-out)                                  |

#### Border Colors

| <div style="min-width: 180px;">Theme Property</div>   | Affected Widgets / Visual Elements                                                                                                         |
| :---------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `borderColor`           | QCheckBox border, QLineEdit border, QMenu border, QToolBar border, QStatusBar border, QGroupBox border, QSplitter, QHeaderView grid lines, table grid lines, frame borders, generic separators |
| `borderColorHovered`    | QCheckBox border hovered                                                                                                                   |
| `borderColorPressed`    | QCheckBox border pressed                                                                                                                   |
| `borderColorDisabled`   | Disabled borders on QCheckBox, QLineEdit, QGroupBox, frames; QMenu separator lines; item view checkbox border (disabled)                   |
| `borderColorTransparent`| Item view checkbox border (checked, selected, disabled – transparent)                                                                      |

#### Semi-Transparent Colors

| <div style="min-width: 230px;">Theme Property</div>    | Affected Widgets / Visual Elements                                             |
| :------------------------------- | :----------------------------------------------------------------------------- |
| `semiTransparentColor1`          | QScrollBar handle (disabled)                                                   |
| `semiTransparentColor2`          | QTab close button hover, QTabBar scroll button hover                           |
| `semiTransparentColor3`          | Reserved – not directly used in current draw code                              |
| `semiTransparentColor4`          | QTab close button pressed, QTabBar scroll button pressed, QScrollBar groove hover/pressed, QScrollBar handle normal |
| `semiTransparentColorTransparent`| QTab close/scroll button normal/disabled, QScrollBar groove normal (invisible) |

---

### Geometry

#### Font Sizes

| Theme Property      | Affected Widgets / Visual Elements                                  |
| :------------------ | :------------------------------------------------------------------ |
| `fontSize`          | Default text size for QLabel, QPushButton, QCheckBox, QComboBox, QLineEdit, QMenu items, and all other standard controls |
| `fontSizeMonospace`  | QPlainTextEdit and QLineEdit when monospace mode is enabled         |
| `fontSizeH1`        | Level 1 heading text (TextRole::H1)                                |
| `fontSizeH2`        | Level 2 heading text (TextRole::H2)                                |
| `fontSizeH3`        | Level 3 heading text (TextRole::H3)                                |
| `fontSizeH4`        | Level 4 heading text (TextRole::H4)                                |
| `fontSizeH5`        | Level 5 heading text (TextRole::H5), QGroupBox title               |
| `fontSizeS1`        | Caption text (TextRole::Caption)                                   |

#### Animation Durations

| <div style="min-width: 170px;">Theme Property</div>   | Affected Widgets / Visual Elements                                                   |
| :----------------------- | :----------------------------------------------------------------------------------- |
| `animationDuration`      | All hover/press/focus state transitions: QPushButton, QCheckBox, QComboBox, QToolButton, QTabBar, QScrollBar thickness, QSlider (programmatic), QDial (programmatic), focus frame |
| `focusAnimationDuration` | Focus ring appear/disappear animation (RoundedFocusFrame)                            |
| `sliderAnimationDuration`| QSlider handle position during user drag, QDial handle during user drag              |

#### Border Radii

| <div style="min-width: 160px;">Theme Property</div>   | Affected Widgets / Visual Elements                                                    |
| :----------------------- | :------------------------------------------------------------------------------------ |
| `borderRadius`           | QPushButton, QComboBox, QSpinBox, QLineEdit, QGroupBox, QTabBar (×1.5 for top corners), QToolButton, QMenu popup, switch, QToolTip, QScrollBar (when margin > 0), QProgressBar |
| `checkBoxBorderRadius`   | QCheckBox indicator, QRadioButton indicator, item view checkboxes, QMenu checkable item indicators |
| `menuItemBorderRadius`   | QMenu item highlight background                                                      |
| `menuBarItemBorderRadius`| QMenuBar item highlight background                                                   |

#### Border & Focus Widths

| <div style="min-width: 160px;">Theme Property</div>    | Affected Widgets / Visual Elements                                                       |
| :---------------- | :--------------------------------------------------------------------------------------- |
| `borderWidth`     | All widget borders: QCheckBox, QLineEdit, QGroupBox, QMenu, QToolBar, QTabBar separators, QSplitter, NavigationBar accent line (×3), separators |
| `focusBorderWidth`| Focus ring thickness on all focusable widgets, also used for focus rect inflation in sizeHint calculations |

#### Control Heights

| <div style="min-width: 160px;">Theme Property</div>    | Affected Widgets / Visual Elements                                                    |
| :------------------- | :------------------------------------------------------------------------------------ |
| `controlHeightLarge` | QPushButton, QComboBox, QLineEdit, QSpinBox, QMenuBar (+ spacing), QTabBar (+ spacing), QToolBar, QTabBar scroll buttons, QScrollBar minimum thumb length, QMenuItem |
| `controlHeightMedium`| QCheckBox/QRadioButton indicator, switch, QProgressBar, QHeaderView sections, NavigationBar items (×2) |
| `controlHeightSmall` | Switch handle component, QMenu scroller, QMenu tear-off handle                        |
| `controlDefaultWidth`| QProgressBar default width, QHeaderView section width (×1.5)                          |

#### Icon Sizes

| <div style="min-width: 160px;">Theme Property</div>     | Affected Widgets / Visual Elements                                                     |
| :----------------- | :------------------------------------------------------------------------------------- |
| `iconSize`         | QPushButton icons, QToolButton icons, QMenu item icons/checkmarks/arrows, QTabBar icons/close buttons/scroll arrows, QSlider handle diameter, tree view branch indicators |
| `iconSizeMedium`   | StatusBadgeWidget, QMenu item icons (standard size)                                    |
| `iconSizeLarge`    | Available for custom use (currently same default as Medium)                             |
| `iconSizeExtraSmall`| Available for minimal icon rendering                                                  |

#### Spacing

| Theme Property | Affected Widgets / Visual Elements                                                               |
| :------------- | :----------------------------------------------------------------------------------------------- |
| `spacing`      | **Universal**: internal padding and margins for all controls. Icon-to-text gaps in buttons, menus, tabs. Layout spacing defaults. QMenu drop shadow gradient width. QScrollBar corner radius. QTabBar extra spacing. |

#### Slider-Specific

| Theme Property       | Affected Widgets / Visual Elements        |
| :------------------- | :---------------------------------------- |
| `sliderGrooveHeight` | QSlider track/groove thickness            |
| `sliderTickSize`     | QSlider tick mark length                  |
| `sliderTickSpacing`  | QSlider gap between groove and tick marks |
| `sliderTickThickness`| QSlider tick mark stroke width            |

#### Dial-Specific

| Theme Property       | Affected Widgets / Visual Elements          |
| :------------------- | :------------------------------------------ |
| `dialGrooveThickness`| QDial arc/groove line width                 |
| `dialTickLength`     | QDial tick mark length                      |
| `dialTickSpacing`    | QDial space between knob edge and ticks     |
| `dialMarkLength`     | QDial needle/value indicator length         |
| `dialMarkThickness`  | QDial needle stroke width                   |

#### Progress Bar

| Theme Property         | Affected Widgets / Visual Elements |
| :--------------------- | :--------------------------------- |
| `progressBarGrooveHeight` | QProgressBar track thickness    |

#### ScrollBar

| Theme Property          | Affected Widgets / Visual Elements                            |
| :---------------------- | :------------------------------------------------------------ |
| `scrollBarThicknessFull`| QScrollBar width when hovered/expanded                        |
| `scrollBarThicknessSmall`| QScrollBar width when idle/collapsed                         |
| `scrollBarMargin`       | QScrollBar margin from parent edge                            |

#### TabBar

| Theme Property     | Affected Widgets / Visual Elements                                   |
| :----------------- | :------------------------------------------------------------------- |
| `tabBarPaddingTop` | Space above tabs within QTabBar, scroll button positioning           |
| `tabBarTabMaxWidth`| Maximum width for a single tab (0 = no limit)                        |
| `tabBarTabMinWidth`| Minimum width for a single tab (0 = no minimum)                      |

#### Fonts & Misc

| Theme Property   | Affected Widgets / Visual Elements                                         |
| :--------------- | :------------------------------------------------------------------------- |
| `useSystemFonts` | When `true`, uses system fonts instead of Qlementine's bundled fonts       |

---

## Theme Colors → QPalette Roles

Qlementine's `Theme::initializePalette()` maps theme colors to `QPalette` roles.
This palette is applied globally via `QApplication::setPalette()` whenever the
theme changes. Widgets that rely on the palette (rather than Qlementine's custom
drawing) use these mappings.

> **Note:** `initializePalette()` is private and only runs during Theme
> construction (default constructor, `fromJsonPath`, `fromJsonDoc`). Mutating
> theme attributes in-place does **not** update the palette — the Theme must be
> reconstructed.

### Shades

| QPalette Role   | Group      | Theme Color            |
| :-------------- | :--------- | :--------------------- |
| `Window`        | All        | `backgroundColorMain2` |
| `Dark`          | All        | `backgroundColorMain3` |
| `Mid`           | All        | `backgroundColorMain3` |
| `Midlight`      | All        | `backgroundColorMain2` |
| `Light`         | All        | `backgroundColorMain2` |

### Item Views

| QPalette Role   | Group      | Theme Color                                                     |
| :-------------- | :--------- | :-------------------------------------------------------------- |
| `Base`          | All        | `backgroundColorMain1`                                          |
| `Base`          | Disabled   | blend(`backgroundColorMain1`, `neutralColorDisabled`)           |
| `AlternateBase` | All        | blend(`backgroundColorMain1`, `neutralColorDisabled` at half α) |
| `AlternateBase` | Disabled   | blend(`backgroundColorMain1`, `neutralColorDisabled`)           |
| `NoRole`        | All        | `backgroundColorMainTransparent`                                |
| `NoRole`        | Disabled   | `backgroundColorMainTransparent`                                |

### Tooltips

| QPalette Role   | Group | Theme Color               |
| :-------------- | :---- | :------------------------ |
| `ToolTipBase`   | All   | `secondaryColor`          |
| `ToolTipText`   | All   | `secondaryColorForeground`|

### Highlight

| QPalette Role     | Group    | Theme Color                 |
| :---------------- | :------- | :-------------------------- |
| `Highlight`       | All      | `primaryColor`              |
| `Highlight`       | Disabled | `primaryColorDisabled`      |
| `HighlightedText` | All      | `primaryColorForeground`    |
| `HighlightedText` | Disabled | `primaryColorDisabled`      |

### Text

| QPalette Role     | Group    | Theme Color                          |
| :---------------- | :------- | :----------------------------------- |
| `Text`            | All      | `secondaryColor`                     |
| `Text`            | Disabled | `secondaryColorDisabled`             |
| `WindowText`      | All      | `secondaryColor`                     |
| `WindowText`      | Disabled | `secondaryColorDisabled`             |
| `PlaceholderText` | All      | `secondaryColorDisabled`             |
| `PlaceholderText` | Disabled | `secondaryColorDisabled`             |
| `Link`            | All      | `primaryColor`                       |
| `Link`            | Disabled | `secondaryColorDisabled`             |
| `LinkVisited`     | All      | `primaryColor`                       |
| `LinkVisited`     | Disabled | `secondaryColorDisabled`             |
| `BrightText`      | All      | `secondaryAlternativeColor`          |
| `BrightText`      | Disabled | `secondaryAlternativeColorDisabled`  |

### Buttons

| QPalette Role | Group    | Theme Color                      |
| :------------ | :------- | :------------------------------- |
| `ButtonText`  | All      | `secondaryColorForeground`       |
| `ButtonText`  | Disabled | `secondaryColorForegroundDisabled`|
| `Button`      | All      | `neutralColor`                   |
| `Button`      | Normal   | `neutralColor`                   |
| `Button`      | Current  | `neutralColorHovered`            |
| `Button`      | Active   | `neutralColorPressed`            |
| `Button`      | Disabled | `neutralColorDisabled`           |

---

## Widget → Theme Properties

For each widget type, this section lists every theme color and geometry value
that affects its rendering.

### QPushButton

| Visual Element       | Theme Property (Normal)            | Hovered                        | Pressed                        | Disabled                        |
| :------------------- | :--------------------------------- | :----------------------------- | :----------------------------- | :------------------------------ |
| Background (primary) | `primaryColor`                     | `primaryColorHovered`          | `primaryColorPressed`          | `primaryColorDisabled`          |
| Background (default) | `neutralColor`                     | `neutralColorHovered`          | `neutralColorPressed`          | `neutralColorDisabled`          |
| Text (primary)       | `primaryColorForeground`           | `primaryColorForegroundHovered`| `primaryColorForegroundPressed`| `primaryColorForegroundDisabled`|
| Text (default)       | `secondaryColor`                   | `secondaryColorHovered`        | –                              | `secondaryColorDisabled`        |
| Focus ring           | `focusColor`                       | –                              | –                              | –                               |
| Drop shadow          | `shadowColor1` / `shadowColor2`    | –                              | –                              | –                               |

| Geometry Property      | Controls                                            |
| :--------------------- | :-------------------------------------------------- |
| `controlHeightLarge`   | Button height                                       |
| `spacing`              | Internal padding, icon-to-text gap                  |
| `borderRadius`         | Corner roundness                                    |
| `borderWidth`          | Border stroke thickness                             |
| `focusBorderWidth`     | Focus ring thickness                                |
| `iconSize`             | Icon dimensions inside button                       |
| `animationDuration`    | Hover/press color transition speed                  |
| `focusAnimationDuration` | Focus ring appear/disappear animation             |

---

### QCheckBox

| Visual Element            | Theme Property (Normal)     | Hovered              | Pressed              | Disabled              |
| :------------------------ | :-------------------------- | :------------------- | :------------------- | :-------------------- |
| Indicator bg (unchecked)  | `backgroundColorMain1`      | –                    | `backgroundColorMain3` | `backgroundColorMain2` |
| Indicator bg (checked)    | `primaryColor`              | `primaryColorHovered`| `primaryColorPressed`| `primaryColorDisabled`|
| Checkmark                 | `primaryColorForeground`    | same                 | same                 | `primaryColorForegroundDisabled` |
| Border (unfocused)        | `borderColor`               | `borderColorHovered` | `borderColorPressed` | `borderColorDisabled` |
| Border (focused)          | `primaryColor`              | –                    | –                    | –                     |
| Focus ring                | `focusColor`                | –                    | –                    | –                     |

| Geometry Property      | Controls                                   |
| :--------------------- | :----------------------------------------- |
| `iconSize`             | Indicator box dimensions                   |
| `checkBoxBorderRadius` | Indicator corner roundness                 |
| `borderWidth`          | Indicator border thickness                 |
| `spacing`              | Gap between indicator and label            |
| `focusBorderWidth`     | Focus ring thickness                       |
| `animationDuration`    | Check/uncheck transition                   |

---

### QRadioButton

Same color mapping as QCheckBox, except the indicator is rendered as a circle
(the `checkBoxBorderRadius` is effectively overridden to produce a full circle).

---

### QComboBox

| Visual Element          | Theme Property (Normal)     | Hovered                | Pressed                | Disabled                |
| :---------------------- | :-------------------------- | :--------------------- | :--------------------- | :---------------------- |
| Background (read-only)  | `neutralColor`              | `neutralColorHovered`  | `neutralColorPressed`  | `neutralColorDisabled`  |
| Background (editable)   | `backgroundColorMain1`      | –                      | –                      | `backgroundColorMain3`  |
| Border (editable)       | `borderColor`               | `borderColorHovered`   | `borderColorPressed`   | `borderColorDisabled`   |
| Text                    | `secondaryColor`            | `secondaryColorHovered`| –                      | `secondaryColorDisabled`|
| Text (status=Error)     | `statusColorError`          | –                      | –                      | –                       |
| Text (status=Warning)   | `statusColorWarning`        | –                      | –                      | –                       |
| Text (status=Success)   | `statusColorSuccess`        | –                      | –                      | –                       |
| Dropdown arrow          | `primaryColor`              | –                      | –                      | –                       |
| Focus ring              | `focusColor`                | –                      | –                      | –                       |

| Geometry Property    | Controls                                        |
| :------------------- | :---------------------------------------------- |
| `controlHeightLarge` | ComboBox height                                 |
| `spacing`            | Padding, icon-to-text gap                       |
| `borderRadius`       | Corner roundness                                |
| `borderWidth`        | Border thickness                                |
| `iconSize`           | Dropdown arrow size                             |
| `focusBorderWidth`   | Focus ring thickness                            |
| `animationDuration`  | State transitions                               |

---

### QSpinBox / QDoubleSpinBox / QDateTimeEdit

| Visual Element        | Theme Property (Normal)    | Hovered              | Pressed              | Disabled              |
| :-------------------- | :------------------------- | :------------------- | :------------------- | :-------------------- |
| Field background      | `backgroundColorMain1`     | –                    | –                    | `backgroundColorMain3`|
| Field border          | `borderColor`              | `borderColorHovered` | `borderColorPressed` | `borderColorDisabled` |
| Field border (focused)| `primaryColor`             | –                    | –                    | –                     |
| Up/down button bg     | `neutralColor`             | `neutralColorHovered`| `neutralColorPressed`| `neutralColorDisabled`|
| Up/down arrow color   | `secondaryColor`           | `secondaryColorHovered`| –                  | `secondaryColorDisabled`|
| Focus ring            | `focusColor`               | –                    | –                    | –                     |

| Geometry Property    | Controls                                        |
| :------------------- | :---------------------------------------------- |
| `controlHeightLarge` | SpinBox height                                  |
| `iconSize`           | Arrow indicator size                            |
| `borderWidth`        | Border and button separator thickness           |
| `borderRadius`       | Field corner roundness                          |
| `spacing`            | Internal padding                                |
| `focusBorderWidth`   | Focus ring thickness                            |
| `animationDuration`  | State transitions                               |

---

### QSlider

| Visual Element         | Theme Property (Normal) | Hovered                    | Pressed                    | Disabled                    |
| :--------------------- | :---------------------- | :------------------------- | :------------------------- | :-------------------------- |
| Groove (unfilled)      | `neutralColor`          | –                          | –                          | `neutralColorDisabled`      |
| Groove (filled/value)  | `primaryColor`          | `primaryColorHovered`      | `primaryColorPressed`      | `primaryColorDisabled`      |
| Handle                 | `primaryColorForeground`| `primaryColorForegroundHovered`| `primaryColorForegroundPressed`| – |
| Handle shadow          | `shadowColor3`          | –                          | –                          | –                           |
| Tick marks             | `borderColor`           | –                          | –                          | `borderColorDisabled`       |

| Geometry Property          | Controls                                     |
| :------------------------- | :------------------------------------------- |
| `sliderGrooveHeight`       | Track/groove thickness                       |
| `sliderTickSize`           | Tick mark length                             |
| `sliderTickSpacing`        | Gap between groove and tick marks            |
| `sliderTickThickness`      | Tick mark stroke width                       |
| `iconSize`                 | Handle (thumb) diameter                      |
| `spacing`                  | Overall padding                              |
| `animationDuration`        | Smooth value animation (programmatic)        |
| `sliderAnimationDuration`  | Quick animation during user drag             |
| `focusBorderWidth`         | Focus ring thickness                         |

---

### QProgressBar

| Visual Element      | Theme Property (Normal) | Disabled                 |
| :------------------ | :---------------------- | :----------------------- |
| Groove (background) | `neutralColor`          | `neutralColorDisabled`   |
| Value (fill)        | `primaryColor`          | `primaryColorDisabled`   |
| Text                | `secondaryColor`        | `secondaryColorDisabled` |

| Geometry Property         | Controls                                  |
| :------------------------ | :---------------------------------------- |
| `progressBarGrooveHeight` | Bar thickness                             |
| `controlHeightMedium`     | Default widget height                     |
| `controlDefaultWidth`     | Default widget width                      |
| `borderRadius`            | Corner roundness of groove and value      |
| `spacing`                 | Text padding                              |

---

### QScrollBar

| Visual Element | Theme Property (Normal)        | Hovered                          | Pressed                          | Disabled              |
| :------------- | :----------------------------- | :------------------------------- | :------------------------------- | :-------------------- |
| Groove (track) | `semiTransparentColorTransparent` | `semiTransparentColor4`       | `semiTransparentColor4`          | –                     |
| Handle (thumb) | `secondaryAlternativeColor`    | `secondaryAlternativeColorHovered`| `secondaryAlternativeColorPressed`| `semiTransparentColor1` |

| Geometry Property         | Controls                                        |
| :------------------------ | :---------------------------------------------- |
| `scrollBarThicknessFull`  | Scrollbar width when hovered/expanded            |
| `scrollBarThicknessSmall` | Scrollbar width when idle/collapsed              |
| `scrollBarMargin`         | Margin between scrollbar and parent edge         |
| `controlHeightLarge`      | Minimum thumb/slider length                      |
| `spacing`                 | Corner radius calculation                        |
| `animationDuration`       | Thickness expand/collapse animation              |

---

### QTabBar / QTabWidget

| Visual Element            | Theme Property (Normal)          | Hovered                | Selected                   | Disabled                       |
| :------------------------ | :------------------------------- | :--------------------- | :------------------------- | :----------------------------- |
| Bar background            | `backgroundColorTabBar`          | –                      | –                          | `backgroundColorMain3`         |
| Tab bg (unselected)       | `neutralColorTransparent`        | `neutralColor`         | –                          | –                              |
| Tab bg (selected)         | –                                | –                      | `backgroundColorMain2`     | –                              |
| Tab text (unselected)     | `secondaryColor`                 | `secondaryColorHovered`| –                          | `secondaryColorDisabled`       |
| Tab text (selected)       | –                                | –                      | `secondaryColor`           | `secondaryColorDisabled`       |
| Close button bg           | `semiTransparentColorTransparent`| `semiTransparentColor2`| –                          | `semiTransparentColorTransparent`|
| Close button icon         | `secondaryColor`                 | `secondaryColor`       | `secondaryColor`           | `secondaryColorTransparent`    |
| Scroll button bg          | `semiTransparentColorTransparent`| `semiTransparentColor2`| `semiTransparentColor4`    | `semiTransparentColorTransparent`|
| Top shadow                | `shadowColor1`                   | –                      | –                          | –                              |
| Bottom shadow             | `shadowColor1`                   | –                      | –                          | –                              |
| Tab separator shadow      | `shadowColor2`                   | –                      | –                          | –                              |

| Geometry Property      | Controls                                           |
| :--------------------- | :------------------------------------------------- |
| `controlHeightLarge`   | Tab height, scroll button height                   |
| `spacing`              | Tab padding, margins, extra internal spacing       |
| `borderRadius`         | Tab corner roundness (×1.5 for top corners)        |
| `borderWidth`          | Tab separators                                     |
| `tabBarPaddingTop`     | Space above tabs within the bar                    |
| `tabBarTabMaxWidth`    | Maximum tab width (0 = unlimited)                  |
| `tabBarTabMinWidth`    | Minimum tab width (0 = no minimum)                 |
| `iconSize`             | Tab icon size, close button size, scroll arrow size|
| `animationDuration`    | Tab state transitions                              |
| `focusBorderWidth`     | Focus indicator                                    |

---

### QMenu

| Visual Element         | Theme Property (Normal)       | Hovered              | Disabled                |
| :--------------------- | :---------------------------- | :------------------- | :---------------------- |
| Menu background        | `backgroundColorMain1`        | –                    | –                       |
| Menu border            | `borderColor`                 | –                    | –                       |
| Menu drop shadow       | `shadowColor1`                | –                    | –                       |
| Item background        | `primaryColorTransparent`     | `primaryColor`       | `primaryColorTransparent`|
| Item text              | `secondaryColor`              | `primaryColorForeground`| `secondaryColorDisabled`|
| Shortcut text          | `secondaryAlternativeColor`   | `primaryColorForegroundHovered`| `secondaryAlternativeColorDisabled`|
| Separator              | `borderColorDisabled`         | –                    | –                       |
| Checkmark bg (checked) | `primaryColor`                | –                    | `primaryColorDisabled`  |
| Checkmark icon         | `primaryColorForeground`      | –                    | `primaryColorForegroundDisabled`|
| Submenu arrow          | `secondaryColor`              | `primaryColorForeground`| `secondaryColorDisabled`|

| Geometry Property       | Controls                                     |
| :---------------------- | :------------------------------------------- |
| `spacing`               | Item padding, icon-text gap, shadow width    |
| `menuItemBorderRadius`  | Item highlight roundness                     |
| `borderRadius`          | Menu popup corner roundness                  |
| `borderWidth`           | Menu border thickness                        |
| `controlHeightSmall`    | Menu scroller/tear-off height                |
| `controlHeightMedium`   | Menu item height                             |
| `iconSize`              | Checkmark, submenu arrow, and item icon size |

---

### QMenuBar

| Visual Element     | Theme Property (Normal)  | Hovered              | Disabled              |
| :----------------- | :----------------------- | :------------------- | :-------------------- |
| Bar background     | `backgroundColorMain2`   | –                    | –                     |
| Item background    | transparent              | `primaryColor`       | –                     |
| Item text          | `secondaryColor`         | `primaryColorForeground`| `secondaryColorDisabled`|

| Geometry Property         | Controls                                 |
| :------------------------ | :--------------------------------------- |
| `controlHeightLarge`      | Bar height (+ spacing)                   |
| `spacing`                 | Item padding                             |
| `menuBarItemBorderRadius` | Item highlight roundness                 |

---

### QToolBar

| Visual Element   | Theme Property           |
| :--------------- | :----------------------- |
| Background       | `backgroundColorMain2`   |
| Bottom border    | `borderColor`            |
| Separator        | `secondaryColorDisabled` |

| Geometry Property    | Controls                |
| :------------------- | :---------------------- |
| `controlHeightLarge` | Toolbar height          |
| `spacing`            | Item spacing            |
| `borderWidth`        | Separator thickness     |

---

### QToolButton

| Visual Element       | Theme Property (Normal)           | Hovered                       | Pressed                       | Disabled                       |
| :------------------- | :-------------------------------- | :---------------------------- | :---------------------------- | :----------------------------- |
| Background           | `neutralColorTransparent` (flat)  | `neutralColor`                | `neutralColorPressed`         | `neutralColorDisabled`         |
| Icon/text color      | `secondaryColor`                  | `secondaryColorHovered`       | –                             | `secondaryColorDisabled`       |
| Menu separator       | `borderColor`                     | `borderColorHovered`          | `borderColorPressed`          | `borderColorDisabled`          |

| Geometry Property    | Controls                                   |
| :------------------- | :----------------------------------------- |
| `controlHeightLarge` | Button height                              |
| `spacing`            | Margins, icon-text gap                     |
| `borderRadius`       | Corner roundness                           |
| `borderWidth`        | Menu separator thickness                   |
| `iconSize`           | Icon dimensions                            |
| `animationDuration`  | State transitions                          |
| `focusBorderWidth`   | Focus ring thickness                       |

---

### QLineEdit

| Visual Element        | Theme Property (Normal)  | Hovered              | Focused              | Disabled              |
| :-------------------- | :----------------------- | :------------------- | :------------------- | :-------------------- |
| Background            | `backgroundColorMain1`   | –                    | –                    | `backgroundColorMain3`|
| Border                | `borderColor`            | `borderColorHovered` | `primaryColor`       | `borderColorDisabled` |
| Border (status=Error) | `statusColorError`       | –                    | `statusColorErrorHovered`| –                |
| Border (status=Warning)| `statusColorWarning`    | –                    | `statusColorWarningHovered`| –              |
| Border (status=Success)| `statusColorSuccess`    | –                    | `statusColorSuccessHovered`| –              |
| Text                  | `secondaryColor`         | –                    | –                    | `secondaryColorDisabled`|
| Placeholder text      | `secondaryAlternativeColor`| –                  | –                    | `secondaryAlternativeColorDisabled`|
| Focus ring            | `focusColor`             | –                    | –                    | –                     |

| Geometry Property    | Controls                                   |
| :------------------- | :----------------------------------------- |
| `spacing`            | Internal padding                           |
| `borderRadius`       | Corner roundness                           |
| `borderWidth`        | Border thickness                           |
| `focusBorderWidth`   | Focus ring thickness                       |
| `animationDuration`  | State transitions                          |

---

### QTextEdit / QPlainTextEdit

Uses the same color and geometry mapping as QLineEdit. Additionally:

- `fontSizeMonospace` is used when monospace mode is enabled.

---

### QGroupBox

| Visual Element | Theme Property (Normal)                    | Disabled                          |
| :------------- | :----------------------------------------- | :-------------------------------- |
| Frame border   | `borderColor`                              | `borderColorDisabled`             |
| Frame fill     | `backgroundColorMain2` + `backgroundColorMain3` (composite) | `backgroundColorMainTransparent` |
| Title text     | `secondaryColor`                           | `secondaryColorDisabled`          |

| Geometry Property      | Controls                              |
| :--------------------- | :------------------------------------ |
| `borderRadius`         | Frame corner roundness                |
| `borderWidth`          | Frame border thickness                |
| `spacing`              | Internal padding                      |

---

### QDial

| Visual Element      | Theme Property (Normal) | Hovered                   | Pressed                   | Disabled                   |
| :------------------ | :---------------------- | :------------------------ | :------------------------ | :------------------------- |
| Circle background   | `neutralColor`          | –                         | –                         | `neutralColorDisabled`     |
| Groove (unfilled)   | `neutralColorPressed`   | –                         | –                         | `neutralColorDisabled`     |
| Groove (filled)     | `primaryColor`          | `primaryColorHovered`     | `primaryColorPressed`     | `primaryColorDisabled`     |
| Handle/knob         | `neutralColor`          | –                         | –                         | `neutralColorDisabled`     |
| Needle mark         | `secondaryColor`        | –                         | –                         | `secondaryColorDisabled`   |
| Tick marks          | `neutralColorPressed`   | –                         | –                         | `neutralColorDisabled`     |
| Handle shadow       | `shadowColor3`          | –                         | –                         | –                          |

| Geometry Property       | Controls                                   |
| :---------------------- | :----------------------------------------- |
| `dialGrooveThickness`   | Arc/groove line width                      |
| `dialTickLength`        | Tick mark length                           |
| `dialTickSpacing`       | Space between knob edge and tick marks     |
| `dialMarkLength`        | Needle/value indicator length              |
| `dialMarkThickness`     | Needle stroke width                        |
| `spacing`               | Overall padding                            |
| `animationDuration`     | Smooth value animation (programmatic)      |
| `sliderAnimationDuration` | Quick animation during user drag         |

---

### QTreeView / QListView / QTableView

| Visual Element              | Theme Property (Normal)        | Hovered              | Selected (active)     | Disabled              |
| :-------------------------- | :----------------------------- | :------------------- | :-------------------- | :-------------------- |
| Row background              | transparent / alternating      | `neutralColor`       | `primaryColor`        | `neutralColorDisabled`|
| Item text                   | `secondaryColor`               | –                    | `primaryColorForeground`| `secondaryColorDisabled`|
| Caption/secondary text      | `secondaryAlternativeColor`    | –                    | `primaryColorForeground`| `secondaryAlternativeColorDisabled`|
| Cell focus border           | –                              | –                    | `primaryColor`        | –                     |
| Checkbox bg (checked)       | `primaryAlternativeColor`      | –                    | –                     | `primaryAlternativeColorDisabled`|
| Checkbox checkmark          | `primaryColorForeground`       | –                    | –                     | `primaryColorForegroundDisabled`|

| Geometry Property      | Controls                                        |
| :--------------------- | :---------------------------------------------- |
| `spacing`              | Cell padding, icon-text gap                     |
| `borderRadius`         | Item background roundness                       |
| `borderWidth`          | Cell borders                                    |
| `controlHeightMedium`  | Default row height                              |
| `iconSize`             | Item icons, branch indicators                   |
| `checkBoxBorderRadius` | In-cell checkbox roundness                      |

---

### QHeaderView

| Visual Element     | Theme Property (Normal)  | Hovered                | Pressed                |
| :----------------- | :----------------------- | :--------------------- | :--------------------- |
| Cell background    | `backgroundColorMain3`   | `neutralColor`         | `neutralColorHovered`  |
| Cell text          | `secondaryColor`         | –                      | –                      |
| Grid lines         | `borderColor`            | –                      | –                      |
| Top shadow         | `shadowColor1`           | –                      | –                      |

| Geometry Property      | Controls                                  |
| :--------------------- | :---------------------------------------- |
| `controlHeightMedium`  | Default header row height                 |
| `controlDefaultWidth`  | Default section width (×1.5)              |
| `spacing`              | Cell padding                              |
| `borderWidth`          | Grid line thickness                       |

---

### QSplitter

| Visual Element | Theme Property (Normal) | Hovered              | Pressed              |
| :------------- | :---------------------- | :------------------- | :------------------- |
| Handle color   | `borderColor`           | `primaryColor`       | `primaryColorHovered`|

| Geometry Property | Controls              |
| :---------------- | :-------------------- |
| `borderWidth`     | Splitter thickness    |

---

### QStatusBar

| Visual Element  | Theme Property           |
| :-------------- | :----------------------- |
| Background      | `backgroundColorMain2`   |
| Top border      | `borderColor`            |
| Item separator  | `secondaryColorDisabled` |

| Geometry Property | Controls               |
| :---------------- | :--------------------- |
| `borderWidth`     | Separator thickness    |
| `spacing`         | Item padding           |

---

### QToolTip

| Visual Element | Theme Property            |
| :------------- | :------------------------ |
| Background     | `secondaryColor`          |
| Border         | `secondaryColorPressed`   |
| Text           | `secondaryColorForeground`|
| Drop shadow    | `shadowColor1` / `shadowColor2` |

| Geometry Property | Controls            |
| :---------------- | :------------------ |
| `spacing`         | Text padding        |
| `borderRadius`    | Corner roundness    |
| `borderWidth`     | Border thickness    |

---

### QFrame

| Visual Element | Theme Property       |
| :------------- | :------------------- |
| Border         | `borderColorDisabled`|
| Separator line | `borderColor`        |

| Geometry Property | Controls           |
| :---------------- | :----------------- |
| `borderWidth`     | Border thickness   |
| `borderRadius`    | Corner roundness   |

---

### QLabel

| Visual Element   | Theme Property (Normal)      | Disabled                         |
| :--------------- | :--------------------------- | :------------------------------- |
| Text             | `secondaryColor`             | `secondaryColorDisabled`         |
| Caption text     | `secondaryAlternativeColor`  | `secondaryAlternativeColorDisabled`|

---

### QDockWidget

Uses QGroupBox-style rendering:

| Visual Element | Theme Property (Normal)  | Disabled              |
| :------------- | :----------------------- | :-------------------- |
| Frame border   | `borderColor`            | `borderColorDisabled` |
| Frame fill     | `backgroundColorMain2`   | –                     |
| Title text     | `secondaryColor`         | `secondaryColorDisabled`|

| Geometry Property | Controls            |
| :---------------- | :------------------ |
| `spacing`         | Padding             |
| `borderRadius`    | Corner roundness    |
| `borderWidth`     | Border thickness    |

---

### Switch (custom Qlementine widget)

| Visual Element     | Theme Property (Normal, unchecked)| Checked (Normal)           | Disabled              |
| :----------------- | :-------------------------------- | :------------------------- | :-------------------- |
| Track background   | `neutralColor`                    | `primaryColor`             | `neutralColorDisabled`/ `primaryColorDisabled`|
| Handle             | `secondaryColor`                  | `primaryColorForeground`   | `secondaryColorDisabled`/ `primaryColorForegroundDisabled`|

| Geometry Property      | Controls                         |
| :--------------------- | :------------------------------- |
| `controlHeightMedium`  | Switch height                    |
| `controlHeightSmall`   | Handle size component            |
| `borderRadius`         | Track and handle roundness       |
| `animationDuration`    | Toggle animation                 |

---

### Focus Frame (all focusable widgets)

The animated focus ring (drawn by `RoundedFocusFrame`) uses:

| Visual Element | Theme Property |
| :------------- | :------------- |
| Ring color     | `focusColor`   |

| Geometry Property         | Controls                              |
| :------------------------ | :------------------------------------ |
| `focusBorderWidth`        | Ring stroke thickness                 |
| `focusAnimationDuration`  | Ring appear/disappear animation speed |

---

## Font Styling

### Bundled Fonts vs System Fonts

By default (`useSystemFonts = false`), Qlementine bundles and uses three font
families. When `useSystemFonts = true`, it falls back to Qt-native system font
queries via `QFontDatabase::systemFont()`.

| Qlementine Font | System Font Fallback                        | Used For                              |
| :-------------- | :------------------------------------------ | :------------------------------------ |
| Inter           | `QFontDatabase::systemFont(GeneralFont)`    | `fontRegular`, `fontBold`, `fontCaption` – all general UI text |
| Inter Display   | `QFontDatabase::systemFont(TitleFont)`      | `fontH1`–`fontH5` – heading/title text |
| Roboto Mono     | `QFontDatabase::systemFont(FixedFont)`      | `fontMonospace` – fixed-width text    |

### The 9 Font Objects

The theme's `fontSize*` values (integers, in **pixels**) are converted to point
sizes via DPI and assigned to pre-built `QFont` objects in
`Theme::initializeFonts()`:

| Font Object     | Base Family   | Weight | Size Source              | Purpose                                       |
| :-------------- | :------------ | :----- | :----------------------- | :-------------------------------------------- |
| `fontRegular`   | Inter         | Normal | `fontSize` (12)          | All standard UI text                          |
| `fontBold`      | Inter         | Bold   | `fontSize` (12)          | Emphasized text (e.g. command button titles)   |
| `fontH1`        | Inter Display | Bold   | `fontSizeH1` (34)        | Heading level 1                               |
| `fontH2`        | Inter Display | Bold   | `fontSizeH2` (26)        | Heading level 2                               |
| `fontH3`        | Inter Display | Bold   | `fontSizeH3` (22)        | Heading level 3                               |
| `fontH4`        | Inter Display | Bold   | `fontSizeH4` (18)        | Heading level 4                               |
| `fontH5`        | Inter Display | Bold   | `fontSizeH5` (14)        | Heading level 5, QGroupBox titles             |
| `fontCaption`   | Inter         | Normal | `fontSizeS1` (10)        | Small caption/label text                      |
| `fontMonospace`  | Roboto Mono  | Normal | `fontSizeMonospace` (13) | Code/fixed-width text                         |

### How Fonts Reach Widgets

There are three paths by which fonts are applied to widgets:

#### 1. Qt-native global default: `QApplication::setFont()`

When the style is applied (in `QlementineStyle::polish(QApplication*)`),
Qlementine calls `QApplication::setFont(theme.fontRegular)`. This is standard
Qt behavior – every widget inherits `fontRegular` unless explicitly overridden.
Any plain `QLabel`, `QPushButton`, `QLineEdit`, etc. automatically gets the
theme font without any Qlementine-specific API.

#### 2. Qlementine `TextRole` enum + `Label` widget

Qlementine defines a `TextRole` enum in `Common.hpp`:

```
Caption = -1, Default = 0, H1, H2, H3, H4, H5
```

The style exposes `fontForTextRole(TextRole)` which maps each role to its
corresponding font object. The custom `Label` widget has a `role` Q_PROPERTY –
setting it automatically applies the correct font and palette (text color):

```cpp
auto* heading = new Label("Section Title", TextRole::H3);
auto* caption = new Label("Fine print", TextRole::Caption);
```

This is the **only** way to use the heading/caption fonts through the theme
system. Standard Qt widgets don't know about `TextRole` – they all use
`fontRegular` via the global font.

#### 3. Hard-coded overrides in draw/polish code

A few places in the style explicitly set fonts during painting or polishing:

| Context                           | Font Used      | How                                      |
| :-------------------------------- | :------------- | :--------------------------------------- |
| QGroupBox title                   | `fontH5`       | Set during `polish(QWidget*)` via `setFont()` |
| QHeaderView selected section      | widget font + bold | Dynamically set bold during `drawControl()` |
| Command button title              | `fontBold`     | Set via `p->setFont()` during painting   |
| Command button description        | `fontRegular`  | Set via `p->setFont()` during painting   |
| QPlainTextEdit (monospace mode)   | `fontMonospace` | Set by Qlementine's custom `PlainTextEdit` widget |
| QLineEdit (monospace mode)        | `fontMonospace` | Set by Qlementine's custom `LineEdit` widget |

### Qt-native vs Qlementine-specific

| Aspect                  | Qt-native                                     | Qlementine-specific                              |
| :---------------------- | :-------------------------------------------- | :----------------------------------------------- |
| Global app font         | `QApplication::setFont()` sets `fontRegular`  | Choice of Inter / Inter Display / Roboto Mono    |
| Widget inherits font    | Yes, all widgets get `fontRegular` automatically | –                                              |
| Heading fonts (H1–H5)  | No Qt equivalent                              | `TextRole` enum + `Label` widget or `fontForTextRole()` |
| Caption font            | No Qt equivalent                              | `TextRole::Caption` + `Label` widget             |
| Monospace font          | Would need manual `setFont()`                 | Custom `LineEdit` / `PlainTextEdit` with monospace mode |
| Bold in specific contexts | Standard `QFont::setBold()`                 | Style hard-codes bold for GroupBox titles, header selections |
| `useSystemFonts` toggle | Uses `QFontDatabase::systemFont()` (Qt API)  | The toggle itself and bundled font fallback are Qlementine |

---

## Icon Theming

Qlementine provides a comprehensive icon colorization and theming system on top
of Qt's built-in `QIcon` infrastructure. The core idea: icons (typically
monochrome SVGs) are automatically recolored to match the theme's foreground
colors, so they stay legible across light/dark themes without shipping multiple
icon variants.

### AutoIconColor – Automatic Icon Colorization

The central concept is the `AutoIconColor` enum (defined in `ImageUtils.hpp`):

```cpp
enum class AutoIconColor {
  None,             // No automatic recolorization – icons drawn as-is
  ForegroundColor,  // Recolorize with the widget's foreground color
  TextColor,        // Recolorize with the palette text color (may differ
                    // from foreground if the palette was customized)
};
```

**Setting it:**

- **Globally** on the style:
  `style->setAutoIconColor(AutoIconColor::ForegroundColor);`
- **Per-widget** (overrides global):
  `QlementineStyle::setAutoIconColor(myButton, AutoIconColor::TextColor);`
  This sets the `"autoIconColor"` dynamic property on the widget.

**Resolution is hierarchical**: when drawing a widget's icon, the style calls
`autoIconColor(widget)` which walks up the parent chain until it finds a widget
with the property set, falling back to the global style setting.

**How it works during painting:**

1. The style retrieves the `QPixmap` from the widget's `QIcon` for the current
   state (normal/disabled/active/selected).
2. It queries `autoIconColor(widget)` to decide what to do.
3. If `None` – pixmap is drawn as-is.
4. If `ForegroundColor` – pixmap is colorized with the theme's foreground color
   (e.g. `secondaryColor` for default buttons, `primaryColorForeground` for
   primary buttons).
5. If `TextColor` – pixmap is colorized with the widget's palette text color
   (which may have been customized independently of the theme).

This pattern is applied consistently in the drawing code for:
QPushButton, QToolButton, QComboBox, QMenu items, item view delegates,
command buttons, and any widget that displays an icon.

### Colorization Modes

Two pixel-level colorization algorithms are available (in `ImageUtils.hpp`):

| Mode | Function | Algorithm | Best For |
| :--- | :------- | :-------- | :------- |
| `Colorize` | `colorizePixmap()` | Replaces all RGB values with the target color, preserving only alpha | Flat/symbolic monochrome icons |
| `Tint` | `tintPixmap()` | Grayscales first, then applies color via Screen composition, preserving luminance and alpha | Complex multi-shade icons |

Both have cached variants (`getColorizedPixmap()` / `getTintedPixmap()`) that
use `QPixmapCache` keyed on the source pixmap + target color. The
`AutoIconColor` system uses `Colorize` mode (via `getColorizedPixmap()`).

### Item View Icon Colorization

Item views (QListView, QTreeView, QTableView) have a dedicated virtual method:

```cpp
virtual AutoIconColor listItemAutoIconColor(
    MouseState mouse, SelectionState selected, FocusState focus,
    ActiveState active, const QModelIndex& index,
    const QWidget* widget) const;
```

The default implementation delegates to `autoIconColor(widget)`, but subclasses
can override it to vary colorization per-item (e.g. colorize selected items
differently, or skip colorization for items that provide their own colored
icons).

When an item is disabled and `AutoIconColor::None` is in effect, the style
composites the icon with the background color to produce a faded appearance.

### Creating Themed Icons

The style provides two convenience methods for creating pre-themed icons:

#### `makeThemedIcon(svgPath, size, role)`

Creates a `QIcon` from an SVG file, pre-colorized for all four `QIcon::Mode`
states (Normal, Disabled, Active, Selected) using the theme's icon foreground
colors for the given `ColorRole` (Primary or Secondary).

Uses `IconTheme` (from `IconUtils.hpp`) which holds four colors:

| IconTheme Field | Secondary role | Primary role |
| :-------------- | :------------- | :----------- |
| `normal` | `secondaryColorForeground` | `primaryColorForeground` |
| `disabled` | `secondaryColorForegroundDisabled` | `primaryColorForegroundDisabled` |
| `checkedNormal` | `secondaryColorForeground` | `primaryColorForeground` |
| `checkedDisabled` | `secondaryColorForegroundDisabled` | `primaryColorForegroundDisabled` |

The resulting `QIcon` has colorized pixmaps baked in for every mode/state, so
it renders correctly without needing `AutoIconColor` at draw time.

#### `makeThemedIconFromName(name, size, role)`

Resolves an icon name to a file path, then delegates to `makeThemedIcon()`.

- If an **icon path getter** function has been set (via
  `setIconPathGetter(func)`), it calls `func(name)` to resolve the name to an
  SVG path.
- If no getter is set, falls back to `QIcon::fromTheme(name)` (Qt's native
  icon theme lookup, e.g. freedesktop icon themes on Linux).

This is how you integrate a custom icon library (like
[qlementine-icons](https://github.com/oclero/qlementine-icons)) – you register
a path getter that maps icon names to your SVG resource paths.

### Icon Sizes from the Theme

The theme defines four icon size tiers:

| Theme Property | Default | Typical Usage |
| :------------- | :------ | :------------ |
| `iconSize` | 16 x 16 | Standard: buttons, menu items, tab icons, tree branches, slider handles |
| `iconSizeMedium` | 24 x 24 | Menu item icons (standard size), status badges |
| `iconSizeLarge` | 24 x 24 | Available for custom use (same default as medium) |
| `iconSizeExtraSmall` | 12 x 12 | Minimal icon rendering |

The `iconSize` value is also used as the QSlider handle diameter.

### Built-in Icon Resources

Qlementine ships a small set of SVG icons for standard Qt dialogs, registered
via `qlementine.qrc`:

| Icon | Used For |
| :--- | :------- |
| `messagebox_critical_bg/fg` | `QMessageBox::Critical` icon |
| `messagebox_information_bg/fg` | `QMessageBox::Information` icon |
| `messagebox_question_bg/fg` | `QMessageBox::Question` icon |
| `messagebox_warning_bg/fg` | `QMessageBox::Warning` icon |

Each icon has a background (`_bg`) and foreground (`_fg`) SVG. The background
is colorized with the status color (e.g. `statusColorError` for critical) and
the foreground with `statusColorForeground`, then composited together. This is
how message box icons automatically match the theme.

Additionally, the style defines extended standard pixmaps via
`StandardPixmapExt`:

| Enum Value | Description |
| :--------- | :---------- |
| `SP_Check` | Checkmark icon (drawn procedurally) |
| `SP_Calendar` | Calendar icon |

### IconWidget

Qlementine provides a custom `IconWidget` (`widgets/IconWidget.hpp`) – a
`QWidget` that displays a `QIcon` with automatic theme-aware colorization.

Properties:

- `icon` – the `QIcon` to display
- `iconSize` – the display size

During painting, it queries the style's `autoIconColor()` for itself, retrieves
the pixmap for the current enabled/disabled state, colorizes it with the
palette text color if auto-colorization is active, and paints it centered.

### Qt-native vs Qlementine-specific

| Aspect | Qt-native | Qlementine-specific |
| :----- | :-------- | :------------------ |
| Icon storage | `QIcon` with mode/state pixmaps | Same, but pixmaps are pre-colorized or colorized at paint time |
| Icon theme lookup | `QIcon::fromTheme()` (freedesktop) | `setIconPathGetter()` for custom resolution, falls back to `fromTheme()` |
| Icon colorization | `QIcon::Mode` (Normal/Disabled/Active/Selected) | `AutoIconColor` system: per-widget/global, hierarchical, two algorithms |
| Drawing icons | `QIcon::paint()` or `QStyle::drawItemPixmap()` | `getPixmap()` + `getColorizedPixmap()` pipeline with DPI-aware caching |
| Per-widget color override | Not available | `setAutoIconColor(widget, mode)` via dynamic property |
| Themed icon creation | Manual `QIcon::addPixmap()` for each mode | `makeThemedIcon()` / `makeThemedIconFromName()` auto-generate all modes |
| Standard dialog icons | Platform-provided | Custom SVGs colorized with theme status colors |
| Icon display widget | `QLabel` with pixmap | `IconWidget` with auto-colorization support |
