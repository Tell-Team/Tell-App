cell_w, cell_h = 10, 12
spacing_x, spacing_y = cell_w + 3, cell_h + 3

num_cols, num_rows = 16, 15
skip_cols, skip_rows = [5, 14], [11]

range_cols = num_cols + len(skip_cols)
range_rows = num_rows + len(skip_rows)

cols = [spacing_x * i for i in range(range_cols) if i + 1 not in skip_cols]
rows = [spacing_y * i for i in range(range_rows) if i + 1 not in skip_rows]

image_w = range_cols * spacing_x + 4
image_h = range_rows * spacing_y + 4 + cell_h

count = 1
with open("teatro_grid.svg", "w") as f:
    teatro_box_h = 12
    f.write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{image_w}" height="{image_h}" viewBox="0 0 {image_w} {image_h}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">\n'
    )
    f.write(
        f'\t<defs>\n    <rect id="cell" width="{cell_w}" height="{cell_h}" fill="gray"/>\n  </defs>\n'
    )
    f.write(
        f"""\t<path d="M3 0v{teatro_box_h}h{image_w-6}v-{teatro_box_h}" fill="gray"></path>
\t<text x="{int(image_w/2)}" y="{int(teatro_box_h/2)}" font-size="8" fill="currentColor" stroke="none" text-anchor="middle" alignment-baseline="middle">Scenario</text>

"""
    )
    for y in rows:
        y = y + 4 + teatro_box_h + 1
        for x in cols:
            x = x + 4
            f.write(f'\t<use href="#cell" x="{x}" y="{y}"/>\n')
            cx = x + cell_w / 2
            cy = y + cell_h / 2 + 1
            f.write(
                f'\t<text x="{cx}" y="{cy}" font-size="5" fill="currentColor" stroke="none" text-anchor="middle" alignment-baseline="middle">{count}</text>\n'
            )
            count += 1
    f.write("</svg>")
