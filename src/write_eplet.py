
import write_svg

def write_stronger_eplet_on_link(svg, path_position, stronger_eplet_on_link):
    already_write = {}
    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1

    for couple, eplets in stronger_eplet_on_link.items():
        for eplet in eplets:
            svg = write_svg.write_text_on_svg(
                svg,
                path_position[couple][0] + 30,
                path_position[couple][1]
                + 0
                + (15 * already_write[couple]),
                font_size=12,
                font_family="Dialog",
                color="#FF0000",
                text=eplet,
            )
            already_write[couple] += 1
    return svg

def write_strong_eplet_on_link(svg, path_position, strong_eplet_on_link):
    already_write = {}
    for couple in strong_eplet_on_link.keys():
        already_write[couple] = 1

    for couple, eplets in strong_eplet_on_link.items():
        for eplet in eplets:
            svg = write_svg.write_text_on_svg(
                svg,
                path_position[couple][0] + 30,
                path_position[couple][1]
                + 0
                + (15 * already_write[couple]),
                font_size=12,
                font_family="Dialog",
                color="#FFA500",
                text=eplet,
            )
            already_write[couple] += 1
    return svg


def write_stronger_eplet_on_bead(svg, bead_position, stronger_eplet_on_bead):
    already_write = {}
    for bead in stronger_eplet_on_bead.keys():
        already_write[bead] = 1

    for bead, eplets in stronger_eplet_on_bead.items():
        for eplet in eplets:
            svg = write_svg.write_text_on_svg(
                svg,
                bead_position[bead][0] + 30,
                bead_position[bead][1]
                + 0
                + (15 * already_write[bead]),
                font_size=12,
                font_family="Dialog",
                color="#FF0000",
                text=eplet,
            )
            already_write[bead] += 1
    return svg

def write_strong_eplet_on_bead(svg, bead_position, strong_eplet_on_bead):
    already_write = {}
    for bead in strong_eplet_on_bead.keys():
        already_write[bead] = 1

    for bead, eplets in strong_eplet_on_bead.items():
        for eplet in eplets:
            svg = write_svg.write_text_on_svg(
                svg,
                bead_position[bead][0] + 30,
                bead_position[bead][1]
                + 0
                + (15 * already_write[bead]),
                font_size=12,
                font_family="Dialog",
                color="#FFA500",
                text=eplet,
            )
            already_write[bead] += 1
    return svg