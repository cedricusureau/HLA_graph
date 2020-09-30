
import write_svg
import math

def write_stronger_eplet_on_link(svg, path_position, stronger_eplet_on_link, text_size):
    global_written = {}
    already_write = {}
    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1

    for couple, eplets in stronger_eplet_on_link.items():
        for eplet in eplets:
            x = path_position[couple][0]
            y = path_position[couple][1] + (text_size * already_write[couple])
            if to_close_to_write(global_written,eplet,"stronger",x,y) == True :
                continue
            else :
                svg = write_svg.write_text_on_svg(
                    svg,
                    x,
                    y,
                    font_size=text_size,
                    font_family="Dialog",
                    color="#FF0000",
                    text=eplet,
                )
                already_write[couple] += 1
                if eplet in global_written.keys():
                    global_written[eplet].append(["stronger",x,y])
                else :
                    global_written[eplet] = [["stronger",x,y]]
    return svg

def write_strong_eplet_on_link(svg, path_position, strong_eplet_on_link, text_size, stronger_eplet_on_link):
    global_written = {}
    already_write = {}
    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1 + len(stronger_eplet_on_link[couple])

    for couple, eplets in strong_eplet_on_link.items():
        for eplet in eplets:
            if already_write[couple] > 2:
                x = path_position[couple][0]
                y = path_position[couple][1] + (text_size * already_write[couple])
                if to_close_to_write(global_written, "...", "stronger", x, y) == True:
                    continue
                else:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        x,
                        y,
                        font_size=text_size,
                        font_family="Dialog",
                        color="#FFA500",
                        text="...",
                    )
                    if "..." in global_written.keys():
                        global_written["..."].append(["strong", x, y])
                    else:
                        global_written["..."] = [["strong", x, y]]
            else:
                x = path_position[couple][0]
                y = path_position[couple][1] + (text_size * already_write[couple])
                if to_close_to_write(global_written, eplet, "strong", x, y) == True:
                    continue
                else:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        x,
                        y,
                        font_size=text_size,
                        font_family="Dialog",
                        color="#FFA500",
                        text=eplet,
                    )
                    already_write[couple] += 1
                    if eplet in global_written.keys():
                        global_written[eplet].append(["strong",x,y])
                    else :
                        global_written[eplet] = [["strong",x,y]]
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

def calculate_distance(pos1, pos2):
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


def to_close_to_write(global_written, text, stronger, x,y):
    to_close = False
    if text in global_written.keys():
        for i in global_written[text]:
            if stronger == i[0]:
                distance = calculate_distance([x,y], [i[1],i[2]])
                if distance < 200:
                    to_close  = True
    return to_close