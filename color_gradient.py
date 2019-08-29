from matplotlib import colors

def colorname_to_hex(name):
    return colors.get_named_colors_mapping()[name]

def hex_to_RGB(hex):
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  RGB_list = [s]
  for t in range(1, n):
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    RGB_list.append(curr_vector)
  return {"hex":[RGB_to_hex(RGB) for RGB in RGB_list]}

def create_gradient(colors, steps, continuous=True):
    colorscale = []
    step = 1
    lastidx = len(colors)-1
    if continuous:
        if (len(colors) - 1) != len(steps) :
            print("Array sizes do not match")
            return colorscale
    else:
        step = 2
        lastidx = len(colors)
        if (len(colors)/2) != len(steps) :
            print("Array sizes do not match")
            return colorscale
    for i in range(0, lastidx, step) :
        c1 = colors[i]
        if c1[0] != '#':
            c1 = colorname_to_hex(c1)
        c2 = colors[i+1]
        if c2[0] != '#':
            c2 = colorname_to_hex(c2)
        s = steps[int(i/step)]
        grad = linear_gradient(c1, c2, s)
        for clr in grad['hex']: 
            colorscale.append(clr)
    return colorscale

#Example usage
colorscale2 = create_gradient(['white', 'black'], [150], True)
colorscale2 = create_gradient(['white', 'green', 'yellow', 'orange', 'red', 'black'], [70,30,50], False)
colorscale2 = create_gradient(['white', 'green', 'lightyellow', 'yellow', 'bisque', 'darkorange'], 
                              [70,30,50], False)
