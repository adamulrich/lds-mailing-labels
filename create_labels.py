from collections import namedtuple
import csv
import labels
from reportlab.graphics import shapes

STATES = {}
with open("state_abbr.csv", newline='') as state_file:
    reader = csv.reader(state_file)
    for row in reader:
        STATES[row[0]] = row[2]

# Create a labels page, matching Avery 5160, 8160, 6240, etc.
PADDING = 1
specs = labels.Specification(
    215.9, 279.4, 3, 10, 64, 25.4, corner_radius=2,
    left_margin=5, right_margin=5, top_margin=13,
    left_padding=PADDING, right_padding=PADDING, top_padding=PADDING,
    bottom_padding=PADDING,
    row_gap=0)

Address = namedtuple(
    'Address',
    ['last_name', 'first_name', 'street1', 'street2', 'city', 'state', 'zip'])


def draw_address(label, width, height, address):
    assert address.state, address
    assert address.zip, address

    # The order is flipped, because we're painting from bottom to top.
    # The Some of the lines get .upper(), because that's what the USPS likes.

    lines = [
        ('%s, %s  %s' % (address.city, STATES[address.state], address.zip)).upper(),
        address.street2.upper(),
        address.street1.upper(),
        '%s %s' % (address.first_name.split(" ")[0], address.last_name)
    ]

    group = shapes.Group()
    x, y = 0, 0
    for line in lines:
        if not line:
            continue
        shape = shapes.String(x, y, line, textAnchor="start")
        _, _, _, y = shape.getBounds()
        # Some extra spacing between the lines, to make it easier to read
        y += 3
        group.add(shape)
    _, _, lx, ly = label.getBounds()
    _, _, gx, gy = group.getBounds()

    # Make sure the label fits in a sticker
    assert gx <= lx, (address, gx, lx)
    assert gy <= ly, (address, gy, ly)

    # Move the content to the center of the sticker
    dx = (lx - gx) / 2
    dy = (ly - gy) / 2
    group.translate(dx, dy)

    label.add(group)


sheet = labels.Sheet(specs, draw_address, border=False)

filename = 'label_data.csv'
with open(filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, Address._fields, quotechar='"')
    for row in reader:
        # Make sure we got all fields, and no extra fields.
        assert None not in row, row['last_name']
        assert 'zip' in row, row['last_name']
        for k, v in row.items():
            row[k] = v.strip()

        address = Address(**row)

        sheet.add_label(address)

sheet.save('labels.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))