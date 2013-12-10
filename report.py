from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import BaseDocTemplate, Paragraph, Image
from reportlab.platypus import Table, TableStyle, flowables
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import FrameBreak, PageTemplate, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.barcode import code128


class FillFrame(Frame):
    def drawBoundary(self, c):
        """
        Draw the rectangles for the header and footer
        This is just for looks
        """
        c.setStrokeColorRGB(.8, .8, .8)
        c.setFillColorRGB(.8, .8, .8)
        c.rect(.125*inch, 7.5*inch, 10.75*inch, .875*inch, fill=1)
        c.rect(.125*inch, .125*inch, 10.75*inch, .825*inch, fill=1)
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(1, 1, 1)
        c.rect(8*inch, 7.625*inch, 2.5*inch, .625*inch, fill=1)
        c.rect(.25*inch, .25*inch, 2.5*inch, .625*inch, fill=1)
        c.setFillColorRGB(0, 0, 0)


class FillFrameHot(Frame):
    def drawBoundary(self, c):
        """
        Draw the rectangles for the header and footer
        This is just for looks
        """
        c.setStrokeColorRGB(.4, .4, .4)
        c.setFillColorRGB(.4, .4, .4)
        c.rect(.125*inch, 7.5*inch, 10.75*inch, .875*inch, fill=1)
        c.rect(.125*inch, .125*inch, 10.75*inch, .825*inch, fill=1)
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(1, 1, 1)
        c.rect(8*inch, 7.625*inch, 2.5*inch, .625*inch, fill=1)
        c.rect(.25*inch, .25*inch, 2.5*inch, .625*inch, fill=1)
        c.setFillColorRGB(0, 0, 0)


def ind_wo(hdata, rows, rowdata, printLoc):
    Title = "Work Order Prints"
    Author = "Ryan Hanson"

    # define frames - for frames in page
    frameFill = FillFrame(x1=.0*inch, y1=0*inch, width=0*inch,
                          height=0*inch, showBoundary=1)
    frameFillHot = FillFrameHot(x1=.0*inch, y1=0*inch, width=0*inch,
                          height=0*inch, showBoundary=1)
    frameHeader = Frame(x1=.25*inch, y1=7.75*inch, width=8*inch, 
                        height=.5*inch)
    frameBarcodeTop = Frame(x1=8*inch, y1=7.375*inch, width=2.5*inch, 
                            height=.875*inch)
    frame1 = Frame(x1=.25*inch, y1=1*inch, width=2.25*inch, height=6.5*inch)
    frame2 = Frame(x1=2.5*inch, y1=1*inch, width=8.5*inch, height=6.5*inch)
    frameFooter = Frame(x1=0*inch, y1=0*inch, width=11*inch, height=1*inch)
    frameBarcodeBottom = Frame(x1=.25*inch, y1=0*inch, width=2.5*inch, 
                               height=.875*inch)
    # define pageTemplates - for page in document
    mainPage = PageTemplate(frames=[frameFill, frameHeader, frameBarcodeTop, 
                                    frame1, frame2, frameFooter, 
                                    frameBarcodeBottom], id="main")
    
    hotPage = PageTemplate(frames=[frameFillHot, frameHeader, frameBarcodeTop, 
                                    frame1, frame2, frameFooter, 
                                    frameBarcodeBottom], id="hot")
    # define BasicDocTemplate - for document
    doc = BaseDocTemplate('indWo.pdf', pagesize=landscape(letter), 
                          leftMargin=72, title=Title, 
                          author=Author, showBoundary=0)
    
    # styles
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleBH = styles["Normal"]
    styleBH.alignment = TA_LEFT

    story = []
    
    #set up header table
    hjob = Paragraph(" Job #:", styleBH)
    hmachine = Paragraph(" Machine:", styleBH)
    hdate_ = Paragraph(" Date:",styleBH)
    job = Paragraph(unicode(hdata[0]), styleBH)
    machine = Paragraph(unicode(hdata[2]), styleBH)
    date_ = Paragraph(unicode(hdata[1]), styleBH)
    header = [[hjob, job, hdate_, date_, hmachine, machine]]
    heading = Table(header, colWidths=[1*inch, 1.5*inch, 1*inch, 
                                       1.5*inch, 1*inch, 1.5*inch])
    heading.hAlign = 'LEFT'
    heading.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), 
                                 ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                 ('BACKGROUND',(1,0),(1,0),colors.white),
                                 ('BACKGROUND',(3,0),(3,0),colors.white),
                                 ('BACKGROUND',(5,0),(5,0),colors.white)]))
    #loop though records
    q=0   
    hot = rowdata[q].value(8).toString()
    if hot == "0": doc.addPageTemplates([mainPage, hotPage])
    else: doc.addPageTemplates([hotPage, mainPage])
    while q<rows:
        
        #Header info and barcode
        story.append(FrameBreak())
        story.append(heading)
        story.append(FrameBreak())
        tracking = unicode(rowdata[q].value(10).toString())
        code = code128.Code128(tracking, barWidth = 1.25)
        code.hAlign = 'CENTER'
        story.append(code)
        textCode = Paragraph(tracking, styleN)
        story.append(textCode)
        story.append(FrameBreak())
        
        #Part data
        hpartNum = Paragraph('''<b>Part #:</b>''', styleBH)
        hqty = Paragraph('''<b>Qty:</b>''', styleBH)
        hdescription = Paragraph('''<b>Description:</b>''', styleBH)
        hmat = Paragraph('''<b>Material:</b>''', styleBH)
        hrouting = Paragraph('''<b>Routing:</b>''', styleBH)
        hdest = Paragraph('''<b>Destination:</b>''', styleBH)
        hnotes = Paragraph('''<b>Notes:</b>''', styleBH)
        horder = Paragraph('''<b>Order:</b>''', styleBH)
        partNum = Paragraph(unicode(rowdata[q].value(0).toString()), styleBH)
        qty = Paragraph(unicode(rowdata[q].value(1).toString()), styleBH)
        description = Paragraph(unicode(rowdata[q].value(2).toString()), styleBH)
        mat = Paragraph(unicode(rowdata[q].value(3).toString()), styleBH)
        routing = Paragraph(unicode(rowdata[q].value(4).toString()), styleBH)
        dest = Paragraph(unicode(rowdata[q].value(5).toString()), styleBH)
        notes = Paragraph(unicode(rowdata[q].value(6).toString()), styleBH)
        order = Paragraph(unicode(rowdata[q].value(9).toString()), styleBH)
        prints = unicode(rowdata[q].value(7).toString())
        
        data= [[hpartNum, partNum],
               [hqty, qty],
               [hdescription, description],
               [hmat, mat],
               [hrouting, routing],
               [hdest, dest],
               [hnotes, notes],
               [horder, order],
               ]
        table = Table(data, colWidths=[1*inch, 1.375*inch])
        table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), 
                                   ('BOX', (0,0), (-1,-1), 0.25, colors.black),]))
        story.append(table)
        story.append(FrameBreak())
        
        #print
        if prints != "":
            prints = "{0}/{1}.jpg".format(printLoc, prints)
            try:
                with open(prints) as f :
                    imgPrint = Image(prints, 8.25*inch, 6.25*inch)
                    story.append(imgPrint)
                    f.close()
            except IOError:
                print "No Print for {0}".format(unicode(prints))
        story.append(FrameBreak())
        story.append(FrameBreak())
        
        #Bottom barcode
        story.append(code)
        story.append(textCode)
        try:
            hot = rowdata[q+1].value(8).toString()
        except:
            hot = "0"
        if hot == "0":
            story.append(NextPageTemplate("main"))
        else:
            story.append(NextPageTemplate("hot"))
        story.append(flowables.PageBreak())
        q += 1

    doc.build(story)
