# Origin style reuse protocol — semantic styling, reproducible data

## Observed vs recommended vs not provided

- Observed in selected OGPO v4 vector plots: bold monospaced typography in many plots; dark red emphasis in some learning curves; semi-transparent bands often near alpha ≈ 0.12 (different in some other figures). Plot settings differ across figures.
- **Recommended adaptations** (stored in `assets/style_profiles.json`): `source_faithful` and `origin_publication`. These are not the original author's code or pixel-exact theme.
- **Not supplied:** native Origin `.oth`, `.otp`, `.otpu` or `.opju` file. This package ships portable style JSON and Matplotlib previews plus manual Origin replication protocol.

## Data → figure contract

Raw learning-curve table (tidy CSV): `panel,series,replicate,x,y`. The `replicate` must denote the declared independent unit (e.g., random training seed); do not silently treat trajectories or video frames as independent seeds.

Output table: `panel,series,x,mean,lower,upper,err_minus,err_plus,n,interval,independent_unit`. Means and nonparametric intervals cannot be inferred from author-provided preaggregated points unless defined by source. If a run fails, don't emit its metric as 0; a valid measured zero remains 0. Unequal replicate grids require explicit pre-specified alignment; default converter rejects them.

### Origin error column interpretation

For a center `m` with interval bounds `[lo,hi]`, set `err_minus=m-lo` and `err_plus=hi-m` **only if both bounds bracket m**. Set error bars with `Value Type=Offset` and one-sided Minus/Plus as appropriate. If bounds do not bracket mean, draw low/high boundary curves with a fill instead; do **not** fake positive offsets. `End Value` is a different Origin mode; document which one your plot uses.

- Color is assigned by **method ID** in R1/R2, by **phase** in R4, by **time** in R5. Do not reuse a palette cyclically with changing category order.
- A shared line legend applies to the same methods across panels. If panels have different metric units use separate linked layers or explicitly independent Y axes, not misleading dual scaling.
- For trajectory plots use equal spatial X/Y scale and preserve disconnected rollouts. For calibration use equal aspect and a y=x diagonal over the plotted range.

## Visual parameter profiles (recommended)

| Property | `source_faithful` | `origin_publication` |
|---|---|---|
| Font | DejaVu Sans Mono / bold | Arial in Origin, DejaVu Sans fallback in preview |
| Single/full width | 88 / 180 mm | 88 / 180 mm |
| Tick label | 8 pt | 8 pt |
| Axis name | 8.5 pt | 9 pt |
| Small title | 9 pt | 9.5 pt |
| Normal/focus stroke | 1.4 / 1.7 pt | 1.4 / 1.8 pt |
| Axis stroke | 0.7 pt | 0.7 pt |
| Interval alpha | 0.12 | 0.12 |

Origin percent transparency = `100 * (1-alpha)`; alpha 0.12 corresponds to **88% transparency**. The opacity is a graphic setting, not uncertainty evidence.

## Reusable Origin process

1. **Prepare:** Use `scripts/prepare_origin_data.py`. Choose exact interval (`none`, sample SD, SEM, or pointwise bootstrap resampling whole independent replicates). Add metadata record and preserve raw measurements.
2. **Import:** Import clean CSV with stable X, Y(center), low, high or negative/positive error offsets; ensure Origin assigns the correct Column Designations and plot grouping.
3. **Plot one representative:** For R1 use Line + Error Band or center line plus two bound curves with Fill Between; set no interval when unknown. Use a semantic palette independent of input row order.
4. **Save distinct assets:** `.oth` theme for appearance; `.otp/.otpu` template for page, layers and plot types; Cloneable template for declared column matching. Avoid storing old task's axis scale/text as reusable style.
5. **Replace data test:** Replace with a differently ordered set of series and checkpoints; check color mapping, X, legend, missing data and units are still right. Do not interpolate missing checkpoints implicitly.
6. **Export final physical size:** Set 88 or 180 mm final width; fix scale factor to 1; inspect rendered fonts and strokes; PDF/SVG vector preferred. Verify transparency, empty margins, panel spacing and accessibility at final view size. Save source project and exported deliverable separately.

Official Origin documentation entry points (may move between versions):

- [Error Band Plot](https://www.originlab.com/doc/Origin-Help/Error-Band-Plot)
- [Graph Template](https://www.originlab.com/doc/Origin-Help/Graph-Template)
- [Set graph size and resolution](https://www.originlab.com/doc/Quick-Help/Set-ExpGraph-Size-Resolution)
- [Plot Details: Error Bar tab](https://www.originlab.com/doc/Origin-Help/PD-Dialog-ErrBar-Tab)

## Tools and limitations

`scripts/render_origin_style.py` renders vector PDF from **actual prepared data**, not invented OGPO curves. Matplotlib is required. This renderer implements R1 learning curves; R2–R8 use the design/Origin recipes, not a claim of complete automatic support.

Finally read the exported data table and plot at 100% physical size. A pretty projection is no substitute for a mechanism diagnostic.
