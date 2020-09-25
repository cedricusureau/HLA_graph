
import write_svg

def write_stronger_eplet_on_link(svg, path_position, stronger_eplet_on_link):
    already_write = {}
    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1

    for couple, eplets in stronger_eplet_on_link.items():
        for eplet in eplets:
            svg = write_svg.write_text_on_svg(
                svg,
                path_position[couple][0],
                path_position[couple][1]
                + (15 * already_write[couple]),
                font_size=16,
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
            if already_write[couple] > 2:
                svg = write_svg.write_text_on_svg(
                    svg,
                    path_position[couple][0],
                    path_position[couple][1] + 15 + (15 * already_write[couple]),
                    font_size=14,
                    font_family="Dialog",
                    color="#FFA500",
                    text="...",
                )
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    path_position[couple][0] ,
                    path_position[couple][1] + 15 + (15 * already_write[couple]),
                    font_size=14,
                    font_family="Dialog",
                    color="#FFA500",
                    text=eplet,
                )
                already_write[couple] += 1
    return svg


def write_stronger_eplet_on_bead(svg, bead_position, stronger_eplet_on_bead, stronger_eplet_on_link):
    already_write = {}
    for bead in stronger_eplet_on_bead.keys():
        already_write[bead] = 1

    stronger_eplet_on_bead = purge_eplet_on_bead(stronger_eplet_on_bead, stronger_eplet_on_link)

    for bead, eplets in stronger_eplet_on_bead.items():
        for eplet in eplets:
            svg = write_svg.write_text_on_svg(
            svg,
            bead_position[bead][0] + 45,
            bead_position[bead][1] + 5
            + (15 * already_write[bead]),
            font_size=16,
            font_family="Dialog",
            color="#FF0000",
            text=eplet,
            )
            already_write[bead] += 1
    return svg

def write_strong_eplet_on_bead(svg, bead_position, strong_eplet_on_bead, strong_eplet_on_link):
    already_write = {}
    for bead in strong_eplet_on_bead.keys():
        already_write[bead] = 1

    strong_eplet_on_bead = purge_eplet_on_bead(strong_eplet_on_bead, strong_eplet_on_link)

    for bead, eplets in strong_eplet_on_bead.items():
        for eplet in eplets:
            if already_write[bead] > 2:
                svg = write_svg.write_text_on_svg(
                    svg,
                    bead_position[bead][0] + 45,
                    bead_position[bead][1]
                    + 20
                    + (15 * already_write[bead]),
                    font_size=16,
                    font_family="Dialog",
                    color="#FFA500",
                    text="...",
                )
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    bead_position[bead][0] + 45,
                    bead_position[bead][1]
                    + 20
                    + (15 * already_write[bead]),
                    font_size=16,
                    font_family="Dialog",
                    color="#FFA500",
                    text=eplet,
                )
                already_write[bead] += 1
    return svg

def purge_eplet_on_bead(eplet_on_bead, eplet_on_link):

    new_eplet_on_bead = {}
    for i,j in eplet_on_bead.items():
        new_eplet_on_bead[i] = list(j)

    for bead, eplets in eplet_on_bead.items():
        for eplet in eplets:
            for couple in eplet_on_link.keys():
                if bead in couple:
                    if eplet in eplet_on_link[couple]:
                        if type(new_eplet_on_bead[bead]) == list:
                            new_eplet_on_bead[bead] = new_eplet_on_bead[bead].remove(eplet)

    for i,j in new_eplet_on_bead.items():
        if j is None:
            new_eplet_on_bead[i] = set()
        else:
            new_eplet_on_bead[i] = set(j)

    return new_eplet_on_bead