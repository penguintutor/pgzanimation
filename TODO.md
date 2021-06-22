#PgzAnimation - Todo list


# Design
Need to determine consistancy with returned values 
(transform vs not transform - points, start, end, rect etc.)

Determine file format for config 

Create a template

Work out best way to include templates (eg. bullet page)

Transparency may need to use unique color and use chromakey
See following example code based on top left pixel

convert logo: -fuzz 25% -fill none -draw "matte 0,0 floodfill" -channel alpha -blur 0x1 -level 50x100% +channel -background saddlebrown -flatten result.jpg

## In progress

Easier layout for creating animations

## Bugs to fix

Frame numbering for saving (skip first frame)

## Testing
Lots more testing is needed