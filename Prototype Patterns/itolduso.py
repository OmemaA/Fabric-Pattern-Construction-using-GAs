def choose_vertices(parent, line, segment, seg_color, orient, upper):
    for iter, i in enumerate(parent.polygons):
            v1 = (line[1][0]-line[0][0], line[1][1]- line[0][1])
            accepted, discarded = [], []
            for x in i:
                v2 = (line[1][0]-x[0], line[1][1]-x[1])
                dot = v1[0]*v2[1] - v1[1]*v2[0]
            if upper:
                if dot >= 0: 
                    accepted.append(x)
                else:
                    discarded.append(x)
            
            elif not upper:
                if dot <= 0:
                    accepted.append(x)
                else:
                    discarded.append(x)

            if len(accepted) > 2:
                segment.append(accepted)
                seg_color.append(parent.colors[iter])
            
            elif len(accepted) > 1:
                for coord in discarded:
                    if (orient):
                        accepted.append((coord[0], line[0][1]))
                    else:
                        accepted.append((line[0][0], coord[1]))
                segment.append(accepted)
                seg_color.append(parent.colors[iter])