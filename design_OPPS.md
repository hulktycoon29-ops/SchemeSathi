# SchemeSathi Website UI Design

## 1. Design Overview

### Purpose

This document defines the visual and animation integration guidance for the website UI, including the supplied React Bits `CursorGrid` and `ElectricBorder` components. It is intended to guide implementation without replacing or modifying the animation component source supplied with the project.

### Visual style

Use a restrained, modern interface with a dark base, readable text, clear spacing, and the supplied cyan electric accent (`#7df9ff`) for electric-border emphasis. The cursor-responsive grid is a subtle background treatment rather than a foreground content element. Keep content contrast and readability ahead of decorative effects.

Do not introduce new UI components beyond the website elements already in scope: header, hero, cards, forms, and the related content/navigation sections already present in the project.

### Layout structure

- **Header:** Site identity and the existing primary navigation.
- **Hero:** Main page heading, concise explanation, and existing primary action.
- **Cards:** Existing scheme/result cards with scheme details and required documents.
- **Forms:** Existing student-input fields for marks, annual family income, and category.
- **Results/content sections:** Display the eligibility output and supporting information using the existing page structure.
- **Background layer:** A `CursorGrid` layer behind the page content.
- **Electric emphasis:** `ElectricBorder` wraps only the existing element(s) chosen for emphasis, such as the primary hero panel or an existing highlighted result card.

### Navigation flow

Use the website's existing navigation flow. A typical SchemeSathi flow is: landing/hero → student details form → eligibility results → required documents for matching schemes. Header links should move to the existing sections or routes; the animation layer must not intercept clicks or alter navigation behavior.

### Global animation principles

- Prefer smooth, restrained motion; animation should support hierarchy rather than compete with content.
- The supplied `CursorGrid` follows the pointer with eased motion and uses a short intro reveal. Its usage example uses `holdTime={400}` and `fadeDuration={800}`.
- The supplied `ElectricBorder` defaults to `speed={1}`, `chaos={0.5}`, `spread={0.6}`, and `flicker={0.5}`. Keep these values unless the design requires a documented prop adjustment.
- Avoid adding a second custom cursor or another competing particle/electric effect.
- Honor `prefers-reduced-motion`. The supplied components already check this preference for parts of their motion; do not remove or bypass that behavior.
- Keep hover/focus feedback quick and consistent with the existing site's interaction styles. Do not animate layout dimensions in a way that causes page reflow.

## 2. Component Design

The following snippets show integration only. Keep the supplied `CursorGrid.jsx`, `CursorGrid.css`, `ElectricBorder.jsx`, and `ElectricBorder.css` source unchanged.

### 2.1 Header

**Layout and styling**

- Keep the existing header structure and navigation items.
- Use a clear background or sufficient contrast so the grid remains subtle behind the header.
- Keep links and buttons above the background layer.
- Maintain the existing responsive behavior and keyboard focus styling.

**Animation**

- No new header-specific animation is required.
- The background grid can respond to pointer movement beneath the header, but the canvas must not capture pointer events.
- Use existing hover/focus styles for navigation links.

Example integration:

```jsx
function SiteLayout({ children }) {
  return (
    <>
      <CursorGrid
        className="site-cursor-grid"
        cellSize={60}
        color="#ffffff"
        highlight="area"
        gridStyle="lines"
        radius={140}
        holdTime={400}
        fadeDuration={800}
        fillOpacity={0.06}
        gridOpacity={0.08}
        spotlight={0.6}
        clickPulse
      />
      <div className="site-content">
        <Header />
        {children}
      </div>
    </>
  );
}
```

This uses the existing `Header` and page content components; it does not define additional UI.

### 2.2 Hero

**Layout and styling**

- Keep the existing headline, supporting text, and primary action.
- Use generous spacing and a readable text width.
- Use the dark background and restrained cyan accent established by the supplied animation components.

**Animation**

- Use the global grid's supplied intro reveal.
- Wrap the existing hero panel with `ElectricBorder` if the hero is intended to be the site's primary visual emphasis.
- Keep the electric effect decorative; it must not cover text or intercept pointer input.

```jsx
import ElectricBorder from "./ElectricBorder";

function Hero() {
  return (
    <section className="hero">
      <ElectricBorder
        color="#7df9ff"
        speed={1}
        chaos={0.5}
        spread={0.6}
        strands={3}
        thickness={1.5}
        borderRadius={24}
      >
        <div className="hero__content">
          {/* Keep the existing hero heading, description, and action here. */}
        </div>
      </ElectricBorder>
    </section>
  );
}
```

The placeholder comment represents the current hero content; do not replace it with new product copy as part of animation integration.

### 2.3 Cards

**Layout and styling**

- Preserve the current card content and information hierarchy.
- Keep scheme name, eligibility result, and required documents easy to scan.
- Match the border radius passed to `ElectricBorder` with the wrapped card's actual radius.

**Animation**

- Use `ElectricBorder` only on an existing highlighted card or result card that needs emphasis.
- Do not wrap every card by default; multiple continuously animated borders can make results harder to scan and increase GPU work.
- Keep ordinary cards static unless the existing design already defines a hover treatment.

```jsx
function HighlightedSchemeCard({ children }) {
  return (
    <ElectricBorder
      color="#7df9ff"
      speed={1}
      chaos={0.5}
      spread={0.6}
      strands={3}
      thickness={1.5}
      borderRadius={24}
    >
      <article className="scheme-card">
        {children}
      </article>
    </ElectricBorder>
  );
}
```

Use this wrapper only where the existing UI already has a card intended for emphasis. The `children` are the existing card contents.

### 2.4 Student details form

**Layout and styling**

- Preserve the existing fields for marks, annual family income, and category.
- Keep labels visible and associated with their inputs.
- Keep validation messages adjacent to the relevant field.
- Ensure controls retain keyboard focus indicators and sufficient contrast.

**Animation**

- The cursor grid may remain visible behind the form but should be subtle enough not to reduce field readability.
- Do not add electric borders to every input. If the existing design includes a highlighted form container, an `ElectricBorder` may wrap that container.
- Animation must not be required to understand validation or submission status.

```jsx
function StudentDetailsSection() {
  return (
    <section className="student-details">
      {/* Keep the existing marks, annual income, and category fields here. */}
      {/* Keep the existing validation and submit behavior unchanged. */}
    </section>
  );
}
```

This section snippet deliberately leaves the existing form implementation unchanged; the animation is applied at the page/background level rather than changing form behavior.

### 2.5 Eligibility results and documents

**Layout and styling**

- Display every scheme returned by the existing eligibility logic.
- Keep required documents grouped with the corresponding scheme.
- Preserve the existing no-match and error states.

**Animation**

- If a result card is already designated as the primary/highlighted result, use the `HighlightedSchemeCard` wrapper above.
- Do not use an electric border to communicate eligibility by itself; eligibility must remain explicit in text.
- Keep result content readable when animation is disabled or WebGL is unavailable.

### 2.6 Existing buttons and links

Keep the existing button and link design. Use the project's existing hover, active, and focus styles. Do not add new animated button effects; the supplied grid already has a click pulse and the electric border can react to pointer proximity and clicks when enabled.

## 3. Background and Global Animations

### 3.1 CursorGrid background

`CursorGrid` draws a grid on a WebGL2 canvas. Cells near the pointer brighten, the grid lines gain a subtle spotlight, and clicks can send a ring pulse through the grid. The component also supports a mount intro animation.

Use the supplied `CursorGrid.jsx` and `CursorGrid.css` files exactly as provided. The component's CSS sets the canvas to `pointer-events: none`, so the page content remains interactive.

### 3.2 Site-wide background configuration

Render the background component once at the application layout/root level, not separately inside every page section.

```jsx
import CursorGrid from "./CursorGrid";
import "./CursorGrid.css";
import "./site-animations.css";

export default function AppLayout({ children }) {
  return (
    <>
      <CursorGrid
        className="site-cursor-grid"
        cellSize={60}
        color="#ffffff"
        highlight="area"
        gridStyle="lines"
        radius={140}
        holdTime={400}
        fadeDuration={800}
        fillOpacity={0.06}
        gridOpacity={0.08}
        spotlight={0.6}
        clickPulse
      />
      <main className="site-content">
        {children}
      </main>
    </>
  );
}
```

If the project already has a root layout component, place the same background instance there rather than creating another layout. Do not render multiple full-screen grid instances on the same page.

### 3.3 Background positioning CSS

Add the following integration CSS in the site's own stylesheet. This is layout CSS for positioning the supplied component; it does not modify `CursorGrid.css`.

```css
.site-cursor-grid {
  position: fixed;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100vh;
  pointer-events: none;
}

.site-content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}
```

Because the background is fixed, it stays in the viewport while the page content scrolls. Keep the content's own backgrounds transparent or appropriately translucent where the grid should show through. Where a section needs an opaque background for legibility, keep that section background as defined by the existing design.

### 3.4 Global background behavior

- `cellSize={60}` controls the grid cell size.
- `radius={140}` controls the cursor's active area.
- `holdTime={400}` and `fadeDuration={800}` control how long cells remain bright and how they fade.
- `fillOpacity={0.06}` and `gridOpacity={0.08}` keep the resting grid subtle.
- `spotlight={0.6}` adds a modest cursor-area glow.
- `clickPulse` enables the supplied click ring effect.

These values follow the provided usage example. Adjust them only through the component props if testing shows a clear usability or performance need.

## 4. Cursor Animation

### 4.1 Effect description

The requested cursor effect is the supplied `CursorGrid` animation, not a replacement system cursor. It highlights grid cells near the pointer, smoothly follows pointer movement, fades recently activated cells, and optionally emits a click pulse. The effect is rendered on a canvas behind the page content.

### 4.2 Attachment

- Import `CursorGrid` and its supplied CSS.
- Mount one instance at the root/layout level for the site-wide effect.
- Use the configuration in Section 3.2.
- Keep the component's `pointer-events: none` canvas styling intact.
- Do not hide the operating system cursor or add a separate trailing cursor element.

### 4.3 Cursor interaction settings

The supplied component supports `highlight="area"` or `highlight="cell"`, multiple `gridStyle` values, different `falloff` curves, and `clickPulse`. The initial configuration uses area highlighting, solid lines, smooth falloff (the component default), and click pulses. Retain these settings unless there is a specific usability reason to change them.

## 5. Electric Board Animation

### 5.1 Effect description

The supplied `ElectricBorder` component creates a moving, irregular electric current around the edge of its child element. It supports glowing strands, flicker, a brief intro race around the border, and a stronger current near the pointer. Clicks inside the active border can trigger a surge.

For this project, “electric board” refers to this electric-border treatment around an existing hero panel or highlighted scheme card. It should be an accent, not a separate panel or new page component.

### 5.2 Placement and trigger points

- **Primary placement:** Existing hero panel, if it is already a distinct panel in the UI.
- **Alternative placement:** One existing highlighted scheme/result card when the results page is shown.
- **Intro trigger:** The supplied component runs its border intro when it mounts, unless disabled through its existing `intro` prop.
- **Pointer trigger:** With `interactive={true}` (the supplied default), the current surges near the pointer within `cursorRadius`.
- **Click trigger:** A click inside an active border can send a surge, provided `active` and `interactive` are enabled.
- **Power control:** `active={false}` can disable the current when the existing page state requires it. Do not introduce unrelated state or new interactions solely to control the effect.

### 5.3 ElectricBorder integration code

Keep the supplied `ElectricBorder.jsx` and `ElectricBorder.css` source unchanged.

```jsx
import ElectricBorder from "./ElectricBorder";
import "./ElectricBorder.css";

function ExistingHighlightedPanel({ children }) {
  return (
    <ElectricBorder
      color="#7df9ff"
      speed={1}
      chaos={0.5}
      spread={0.6}
      strands={3}
      thickness={1.5}
      borderRadius={24}
    >
      {children}
    </ElectricBorder>
  );
}
```

Wrap an existing panel with `ExistingHighlightedPanel` only if that panel is already part of the page design. Keep the panel's existing contents and behavior.

### 5.4 ElectricBorder prop guidance

| Prop | Initial value | Purpose |
|---|---:|---|
| `color` | `"#7df9ff"` | Cyan current color. |
| `speed` | `1` | Current movement speed. |
| `chaos` | `0.5` | Jaggedness of the strands. |
| `spread` | `0.6` | Distance the current wanders from the edge. |
| `strands` | `3` | Number of current strands. |
| `thickness` | `1.5` | Strand thickness in pixels. |
| `borderRadius` | `24` | Must match the wrapped panel's radius. |
| `active` | `true` | Turns the current on or off. |
| `intro` | `true` | Enables the mount intro animation. |
| `interactive` | `true` | Enables pointer and click reactions. |
| `cursorRadius` | `90` | Pointer interaction radius. |

Do not add a separate “electric board” DOM or canvas implementation. Use the supplied component for this effect.

## 6. Implementation Guidance

### 6.1 Files

Keep the supplied animation files separate from the site's own layout CSS:

```text
src/
  components/
    CursorGrid.jsx
    CursorGrid.css
    ElectricBorder.jsx
    ElectricBorder.css
  styles/
    site-animations.css
  ...existing site files...
```

This is a suggested placement for the supplied files; use the project's existing folder conventions if they differ. Do not rewrite or reformat the component source while integrating it.

### 6.2 Dependencies and browser support

- **React:** Required by both components.
- **WebGL 2:** Required by the supplied canvas shader implementations.
- **Browser APIs used by the supplied components:** `requestAnimationFrame`, `ResizeObserver`, `IntersectionObserver`, `matchMedia`, and pointer/visibility events.
- **CSS:** Import each component's supplied stylesheet.
- **Additional animation library:** None is required for these two effects.

The components request a `webgl2` context. If a browser/device does not support WebGL2 or shader initialization fails, the animation may not render. The surrounding UI must remain usable without it. Do not assume the supplied source automatically provides a visual fallback for every failure mode.

### 6.3 Performance

- Render only one site-wide `CursorGrid` instance.
- Use `ElectricBorder` selectively rather than on every card.
- Keep `ambient` at its default of `0` unless ambient activity is explicitly needed.
- Avoid unnecessarily small `cellSize` values, which increase the number of grid cells.
- Keep animated areas to the minimum required by the design.
- Preserve the supplied use of `requestAnimationFrame`, resize/intersection observers, and page-visibility handling.
- Test on a lower-powered device as well as a desktop.
- Watch GPU usage and frame stability when both effects are visible simultaneously.

### 6.4 Accessibility and reduced motion

- Keep all meaningful content as normal HTML; the canvas is decorative and must not be the only way to convey information.
- Keep keyboard navigation and focus indicators visible.
- Do not use the electric effect alone to signal success, eligibility, errors, or focus.
- Preserve the supplied `prefers-reduced-motion` checks. Test the website with the operating system's reduced-motion preference enabled.
- Ensure the page works when the animation is unavailable or disabled.

### 6.5 Cross-browser compatibility

- Test in current browsers that support WebGL2.
- Check browser console output for shader compilation or WebGL context errors.
- Test resizing, scrolling, pointer exit, tab visibility changes, and route transitions.
- Avoid depending on the animation for layout measurements or application logic.
- Ensure the CSS stacking order keeps content above the grid and the electric canvas above neither text nor interactive controls. The supplied electric canvas uses `pointer-events: none`.

### 6.6 Integration checklist

- [ ] The supplied `CursorGrid` source is copied without changes.
- [ ] The supplied `CursorGrid.css` is imported.
- [ ] Exactly one site-wide grid is mounted.
- [ ] The background sits behind all existing page content.
- [ ] The supplied `ElectricBorder` source is copied without changes.
- [ ] The supplied `ElectricBorder.css` is imported.
- [ ] The electric effect wraps only an existing hero panel or highlighted card.
- [ ] Header links, form fields, buttons, and cards remain interactive.
- [ ] Eligibility and document information remain readable without animation.
- [ ] Reduced-motion and WebGL2-unavailable scenarios are tested.
- [ ] No additional cursor or electric animation implementation has been introduced.

## 7. Assumptions and Notes

- The supplied files define the animation behavior and are the source of truth for component props and implementation.
- The existing website components and content remain in place; this document specifies where to integrate the two animations, not a redesign of those components.
- The exact project framework setup and file paths may differ. Update import paths to match the repository while keeping component source unchanged.
- The provided component snippets are integration examples and assume the named existing components (`Header`, hero content, and result cards) are already defined.
- The background grid and electric border are decorative enhancements. They must never change eligibility calculations, navigation, form submission, or report behavior.
