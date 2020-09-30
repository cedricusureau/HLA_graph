
import write_svg

def write_stronger_eplet_on_link(svg, path_position, stronger_eplet_on_link, text_size):
    global_written = {}
    already_write = {}
    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1

    for couple, eplets in stronger_eplet_on_link.items():
        for eplet in eplets:

            svg = write_svg.write_text_on_svg(
                svg,
                path_position[couple][0],
                path_position[couple][1]
                + (text_size * already_write[couple]),
                font_size=text_size,
                font_family="Dialog",
                color="#FF0000",
                text=eplet,
            )
            already_write[couple] += 1
            if eplet in global_written.keys():
                global_written[eplet].append(["stronger",path_position[couple][0],path_position[couple][1]])
            else :
                global_written[eplet] = [["stronger",path_position[couple][0],path_position[couple][1]]]
    return svg, global_written

def write_strong_eplet_on_link(svg, path_position, strong_eplet_on_link, text_size, stronger_eplet_on_link):

    already_write = {}
    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1 + len(stronger_eplet_on_link[couple])

    for couple, eplets in strong_eplet_on_link.items():
        for eplet in eplets:
            if already_write[couple] > 2:

                svg = write_svg.write_text_on_svg(
                    svg,
                    path_position[couple][0],
                    path_position[couple][1] + (text_size * already_write[couple]),
                    font_size=text_size,
                    font_family="Dialog",
                    color="#FFA500",
                    text="...",
                )
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    path_position[couple][0] ,
                    path_position[couple][1] + (text_size * already_write[couple]),
                    font_size=text_size,
                    font_family="Dialog",
                    color="#FFA500",
                    text=eplet,
                )
                already_write[couple] += 1
    return svg


def write_stronger_eplet_on_bead(svg, bead_position, stronger_eplet_on_bead, stronger_eplet_on_link, text_size, text_position):
    already_write = {}

    for bead in stronger_eplet_on_bead.keys():
        already_write[bead] = 1

    stronger_eplet_on_bead = purge_eplet_on_bead(stronger_eplet_on_bead, stronger_eplet_on_link)

    for bead, eplets in stronger_eplet_on_bead.items():
        for eplet in eplets:
            svg = write_svg.write_text_on_svg(
            svg,
            bead_position[bead][0] + text_position[0],
            bead_position[bead][1] + text_position[1]
            + (text_size * already_write[bead]),
            font_size=text_size,
            font_family="Dialog",
            color="#FF0000",
            text=eplet,
            )
            already_write[bead] += 1
    return svg

def write_strong_eplet_on_bead(svg, bead_position, strong_eplet_on_bead, stronger_eplet_on_bead, strong_eplet_on_link, text_size, text_position):
    already_write = {}

    strong_eplet_on_bead = purge_eplet_on_bead(strong_eplet_on_bead, strong_eplet_on_link)
    for bead in stronger_eplet_on_bead.keys():
        already_write[bead] = 1 + len(stronger_eplet_on_bead[bead])

    for bead, eplets in strong_eplet_on_bead.items():
        for eplet in eplets:
            if already_write[bead] > 2:
                svg = write_svg.write_text_on_svg(
                    svg,
                    bead_position[bead][0] + text_position[0],
                    bead_position[bead][1] + text_position[1]
                    + (text_size * already_write[bead]),
                    font_size=text_size,
                    font_family="Dialog",
                    color="#FFA500",
                    text="...",
                )
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    bead_position[bead][0] + float(text_position[0]),
                    bead_position[bead][1] + float(text_position[1])
                    + (text_size * already_write[bead]),
                    font_size=text_size,
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
                            if eplet in new_eplet_on_bead[bead]:
                                new_eplet_on_bead[bead].remove(eplet)

    for i,j in new_eplet_on_bead.items():
        if j is None:
            new_eplet_on_bead[i] = set()
        else:
            new_eplet_on_bead[i] = set(j)

    return new_eplet_on_bead


def write_A_or_B_eplets(svg, A_eplet, B_eplet, all_written_stronger, all_written_strong, allele_type):
    pos_x, pos_y = -900, -1100
    count_A = 1
    count_B = 1
    already_write_suspension_A = False
    already_write_suspension_B = False
    if allele_type == "DP":
        pos_x, pos_y = -1200, -1400


    svg = write_svg.write_text_on_svg(
        svg,
        pos_x,
        pos_y,
        font_size=40,
        font_family="Dialog",
        color="#1f618d",
        text="{}A: ".format(allele_type),
    )

    svg = write_svg.write_text_on_svg(
        svg,
        pos_x,
        pos_y + 50,
        font_size=40,
        font_family="Dialog",
        color="#196f3d",
        text="{}B: ".format(allele_type),
    )

    for eplet in all_written_stronger:
        if eplet in A_eplet:
            if count_A > 36 :
                if already_write_suspension_A == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (50 + 30 * count_A + 10 * len("...")),
                        pos_y,
                        font_size=36,
                        font_family="Dialog",
                        color="#FF0000",
                        text="...",
                    )

                    already_write_suspension_A = True
                else :
                    continue
            else :
                svg = write_svg.write_text_on_svg(
                    svg,
                    pos_x + ( 50 + 30 * count_A + 10 * len(eplet)),
                    pos_y,
                    font_size=36,
                    font_family="Dialog",
                    color="#FF0000",
                    text=eplet,
                )
                count_A += len(eplet)
        elif eplet in B_eplet:
            if count_B > 36:
                if already_write_suspension_B == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (50 + 30 * count_B + 10 * len("...")),
                        pos_y + 50,
                        font_size=36,
                        font_family="Dialog",
                        color="#FF0000",
                        text="...",
                    )
                    already_write_suspension_B = True
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    pos_x + (50 + 30 * count_B +  10 * len(eplet)),
                    pos_y + 50,
                    font_size=36,
                    font_family="Dialog",
                    color="#FF0000",
                    text=eplet,
                )
                count_B += len(eplet)
        else: print("oups")

    for eplet in all_written_strong:
        if eplet in A_eplet:
            if count_A > 36:
                if already_write_suspension_A == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (50 + 30 * count_A + 10 * len("...")),
                        pos_y,
                        font_size=36,
                        font_family="Dialog",
                        color="#FFA500",
                        text="...",
                    )
                    already_write_suspension_A = True
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    pos_x + ( 50 + 30 * count_A + 10 * len(eplet)),
                    pos_y,
                    font_size=36,
                    font_family="Dialog",
                    color="#FFA500",
                    text=eplet,
                )
                count_A += len(eplet)
        elif eplet in B_eplet:
            if count_B > 36:
                if already_write_suspension_B == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (50 + 30 * count_B + 10 * len("...")),
                        pos_y + 50,
                        font_size=36,
                        font_family="Dialog",
                        color="#FFA500",
                        text="...",
                    )
                    already_write_suspension_B = True
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    pos_x + (50 + 30 * count_B +  10 * len(eplet)),
                    pos_y + 50,
                    font_size=36,
                    font_family="Dialog",
                    color="#FFA500",
                    text=eplet,
                )
                count_B += len(eplet)
        else: print("oups")
    return svg