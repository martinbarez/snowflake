from math import sqrt


def colour(cell):
    if cell.attached:
        mass = cell.crystal_mass
    else:
        mass = cell.diffusive_mass
    c = 255 - 128 * mass  # mass < 2
    c = max(0, int(c))
    return hex(c)[2:]*3


def save_svg(automata, filename):
    # optimize undisturbed cells away by computing the density
    # of background vapor
    aux = lambda: None
    aux.diffusive_mass = automata.params["rho"]
    aux.attached = False
    background = colour(aux)

    with open(filename, "w") as f:
        side = sqrt(3)  # width - height relationship
        y_margin = (automata.size-int(automata.size*side/2))//2  # square
        snowflake_h = automata.size*3-y_margin
        snowflake_w = int(automata.size*3)
        textrect_h = automata.size//15
        text_y = snowflake_h + textrect_h-automata.size/60
        font_size = automata.size//20

        f.write(f'<svg version="1.1" width="{snowflake_w}" height="{snowflake_h+textrect_h}" xmlns="http://www.w3.org/2000/svg">')
        f.write(f'<rect width="100%" height="100%" shape-rendering="optimizespeed" fill="#{background}"/>')
        for j in range(y_margin, automata.size-y_margin):
            for i in range(automata.size):
                # middle point of hexagon
                x = i*3+1.5
                y = (j-y_margin)*2*side+(i%2)*side
                c = colour(automata.cells[j*automata.size+i])
                if c != background:
                    f.write(f'<polygon points="{x-1},{y-side} {x+1},{y-side} {x+2},{y} {x+1},{y+side} {x-1},{y+side} {x-2},{y}" style="fill:#{c}" stroke="#{c}" stroke-width="0.1" />')
        f.write(f'<rect width="{snowflake_w}" height="{textrect_h}" x="0" y="{snowflake_h}" fill="white"/>')
        f.write(f'<text x="0" y="{text_y}" font-family="sans-serif" font-size="{font_size}">\
            &#160;&#160;&#160;&#160;\
            {automata.size}x{automata.size}&#160;&#160;&#160;&#160;\
            {automata.iteration} Generations&#160;&#160;&#160;&#160;\
            ρ:{automata.params["rho"]} &#160;\
            β:{automata.params["beta"]} &#160;\
            α:{automata.params["alpha"]} &#160;\
            θ:{automata.params["theta"]} &#160;\
            κ:{automata.params["kappa"]} &#160;\
            µ:{automata.params["mu"]} &#160;\
            γ:{automata.params["upsilon"]} &#160;\
            σ:{automata.params["sigma"]}</text>')
        f.write('</svg>')
