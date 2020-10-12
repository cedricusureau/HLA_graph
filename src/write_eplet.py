
import src.write_svg as write_svg
import math

def write_stronger_eplet_on_link(svg, path_position, stronger_eplet_on_link, text_size, bead_text_position):
    global_written = {}
    already_write = {}
    warning = False
    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1

    for couple, eplets in stronger_eplet_on_link.items():
        for eplet in eplets:

            x = path_position[couple][0]
            y = path_position[couple][1] + (text_size * already_write[couple]) - 30
            if to_close_to_write(global_written,eplet,x,y, bead_text_position) == True :
                if warning == False :
                    view_box = get_view_box(svg)
                    svg_list = write_warning_message(view_box, svg)
                    warning = True
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
    return svg, global_written

def write_strong_eplet_on_link(svg, path_position, strong_eplet_on_link, text_size, stronger_eplet_on_link, bead_text_position, global_written_stronger_link):
    global_written = global_written_stronger_link
    already_write = {}
    warning = False

    for couple in stronger_eplet_on_link.keys():
        already_write[couple] = 1 + len(stronger_eplet_on_link[couple])

    for couple, eplets in strong_eplet_on_link.items():
        for eplet in eplets:
            if already_write[couple] > 2:
                x = path_position[couple][0]
                y = path_position[couple][1] + (text_size * already_write[couple]) - 30
                if to_close_to_write(global_written, "...", x, y, bead_text_position) == True:
                    if warning == False:
                        view_box = get_view_box(svg)
                        svg_list = write_warning_message(view_box, svg)
                        warning = True
                    continue
                else:
                    if warning == False:
                        view_box = get_view_box(svg)
                        svg_list = write_warning_message(view_box, svg)
                        warning = True
                    svg = write_svg.write_text_on_svg(
                        svg,
                        x,
                        y,
                        font_size=text_size,
                        font_family="Dialog",
                        color="#1e8449",
                        text="...",
                    )
                    if "..." in global_written.keys():
                        global_written["..."].append(["strong", x, y])
                    else:
                        global_written["..."] = [["strong", x, y]]
            else:
                x = path_position[couple][0]
                y = path_position[couple][1] + (text_size * already_write[couple]) - 30
                if to_close_to_write(global_written, eplet, x, y, bead_text_position) == True:
                    if warning == False:
                        view_box = get_view_box(svg)
                        svg_list = write_warning_message(view_box, svg)
                        warning = True
                    continue
                else:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        x,
                        y,
                        font_size=text_size,
                        font_family="Dialog",
                        color="#1e8449 ",
                        text=eplet,
                    )
                    already_write[couple] += 1
                    if eplet in global_written.keys():
                        global_written[eplet].append(["strong",x,y])
                    else :
                        global_written[eplet] = [["strong",x,y]]
    return svg, global_written


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
    warning = False

    strong_eplet_on_bead = purge_eplet_on_bead(strong_eplet_on_bead, strong_eplet_on_link)
    for bead in stronger_eplet_on_bead.keys():
        already_write[bead] = 1 + len(stronger_eplet_on_bead[bead])

    for bead, eplets in strong_eplet_on_bead.items():
        for eplet in eplets:
            if already_write[bead] > 2:
                if warning == False :
                    view_box = get_view_box(svg)
                    svg_list = write_warning_message(view_box, svg)
                    warning = True
                svg = write_svg.write_text_on_svg(
                    svg,
                    bead_position[bead][0] + text_position[0],
                    bead_position[bead][1] + text_position[1]
                    + (text_size * already_write[bead]),
                    font_size=text_size,
                    font_family="Dialog",
                    color="#52be80 ",
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
                    color="#52be80 ",
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
    pos_x, pos_y = -900, -1200
    count_A = 1
    count_B = 1
    already_write_suspension_A = False
    already_write_suspension_B = False
    if allele_type == "DP":
        pos_x, pos_y = -1150, -1250


    svg = write_svg.write_text_on_svg(
        svg,
        pos_x,
        pos_y,
        font_size=50,
        font_family="Dialog",
        color="#1b2631",
        text="{}A: ".format(allele_type),
    )

    svg = write_svg.write_text_on_svg(
        svg,
        pos_x,
        pos_y + 50,
        font_size=46,
        font_family="Dialog",
        color="#1b2631",
        text="{}B: ".format(allele_type),
    )

    for eplet in all_written_stronger:
        if eplet in A_eplet:
            if count_A > 20 :
                if already_write_suspension_A == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (60 + 40 * count_A + 10 * len("...")),
                        pos_y,
                        font_size=46,
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
                    pos_x + (60 + 40 * count_A + 10 * len(eplet)),
                    pos_y,
                    font_size=46,
                    font_family="Dialog",
                    color="#FF0000",
                    text=eplet,
                )
                count_A += len(eplet)
        elif eplet in B_eplet:
            if count_B > 20:
                if already_write_suspension_B == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (60 + 40 * count_B + 10 * len("...")),
                        pos_y + 50,
                        font_size=46,
                        font_family="Dialog",
                        color="#FF0000",
                        text="...",
                    )
                    already_write_suspension_B = True
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    pos_x + (60 + 40 * count_B +  10 * len(eplet)),
                    pos_y + 50,
                    font_size=46,
                    font_family="Dialog",
                    color="#FF0000",
                    text=eplet,
                )
                count_B += len(eplet)
        else: print("oups")

    for eplet in all_written_strong:
        if eplet in A_eplet:
            if count_A > 20:
                if already_write_suspension_A == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (60 + 40 * count_A + 10 * len("...")),
                        pos_y,
                        font_size=46,
                        font_family="Dialog",
                        color="#1e8449 ",
                        text="...",
                    )
                    already_write_suspension_A = True
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    pos_x + ( 60 + 40* count_A + 10 * len(eplet)),
                    pos_y,
                    font_size=46,
                    font_family="Dialog",
                    color="#1e8449 ",
                    text=eplet,
                )
                count_A += len(eplet)
        elif eplet in B_eplet:
            if count_B > 20:
                if already_write_suspension_B == False:
                    svg = write_svg.write_text_on_svg(
                        svg,
                        pos_x + (60 + 40 * count_B + 10 * len("...")),
                        pos_y + 50,
                        font_size=46,
                        font_family="Dialog",
                        color="#1e8449 ",
                        text="...",
                    )
                    already_write_suspension_B = True
            else:
                svg = write_svg.write_text_on_svg(
                    svg,
                    pos_x + (60 + 40 * count_B +  10 * len(eplet)),
                    pos_y + 50,
                    font_size=46,
                    font_family="Dialog",
                    color="#1e8449 ",
                    text=eplet,
                )
                count_B += len(eplet)

    return svg

def calculate_distance(pos1, pos2):
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


def to_close_to_write(global_written, text, x,y, bead_text_position):
    to_close = False
    for text2, value in global_written.items():
        if text == text2:
            for i in value:
                distance = calculate_distance([x,y], [i[1],i[2]])
                if distance < 120:
                    to_close  = True

    for i in bead_text_position:
        distance = calculate_distance([x,y], [i[0], i[1]])
        if distance < 80:
            to_close = True
    return to_close

def check_couple_order(couple_dict, path_position):
    new_couple_dict = {}
    for couple, eplets in couple_dict.items():
        if couple not in path_position.keys():
            new_couple_dict[couple.split(" ")[1]+" "+couple.split(" ")[0]] = eplets
        else :
            new_couple_dict[couple] = eplets
    return new_couple_dict

def get_view_box(mfi):
    for i in mfi:
        if 'viewBox="' in i :
            return [int(k) for k in i.replace('   viewBox="','').replace('"\n','').split(" ")]

def write_warning_message(view_box, svg):
    svg = write_svg.write_text_on_svg(
        svg,
        view_box[0] + 480,
        view_box[1] + view_box[3] - 180,
        font_size=46,
        font_family="Dialog",
        color="#ba4a00",
        text="Some positive eplets are not displayed."
    )
    svg = write_svg.write_text_on_svg(
        svg,
        view_box[0] + 480,
        view_box[1] + view_box[3] - 180 + 46,
        font_size=46,
        font_family="Dialog",
        color="#ba4a00",
        text="Please check raw data."
    )
    return svg