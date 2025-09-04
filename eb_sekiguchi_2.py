#!/usr/bin/env python
# -*- coding:utf-8 -*-
## @package MagLib.eblitho
#
# Creates EB lithography command files (.CC6)
#このファイルの単位はnm

import numpy as np
from dxfwrite import DXFEngine as dxf


## Writer class for EB lithography command files (.CC6)
#
#  Also creates CAD file (.dxf).
#  HOWTO BASIC:
#  1. Create class instance: hoge = CC6Writer()
#  2. Set filename (used for both CC6 and dxf): hoge.open(your_filename_here)
#  2. Use the various drawing functions
#  3. Close the file: hoge.close()
class CC6Writer:
    def __init__(self): #__init__でobjectの初期設定を行う
        self._unit = 300000 / 60000  # Unit length per EB drawing cell (nm) #s self._でインスタンス変数 # field_size/number_of_dots
        self._patchSize = 300000  # Size of single patch(nm)(=field_size)
        self._errorCount = 0  # Number of commands with errors
        self._commandCount = 0  # Total number of commands
        self._maxCommand = 16000000  # Maximum limit of command counts
        self._doseTimeMin = 0.1  # Minimum dose time of EB (μsec.)
        self._doseTimeMax = 3200  # Maximum dose time of EB (μsec.)
        self._cc6Lines = []

    ## Open new file.
    #
    # This is the first function to be called after class instantiation.
    # Note: dxffast is available as faster option, but may not work if
    # there are changes to how dxfwrite is used.
    # @param fileName The output filename for CC6, dxf, and log file.
    
    def open(self, fileName):
        # Create CC6, write first line
        self._cc6File = open(fileName + ".CC6", "w")
        self._cc6File.write("PATTERN\r\n")  # line end is CR (\x0D) + LF (\x0A)

       
        # Create dxf file
        self._drawing = dxf.drawing(fileName + ".dxf")

        # Create log text
        self._logFile = open(fileName + "_log.txt", "w")

    ## Close all written files to finalize.
    def close(self):
        # Write final line and close CC6 file
        self._cc6File.write("END\r\n")
        self._cc6File.write("\x1A")  # Ctrl-Z sequence
        self._cc6File.close()

        # Close dxf file
        self._drawing.save()

        # Write out log output and close log file
        self._log("Objects: %10d" % self._commandCount)
        self._log("Errors:  %10d" % self._errorCount)
        if self._commandCount > self._maxCommand:
            self._log(
                "Number of objects exceeded maximum limit. "
                "Please do not use this file."
            )
        self._logFile.close()

    ## Outpus log to both screen and log file
    def _log(self, info):
        print(info)
        self._logFile.write("%s\r\n" % info)

    ## Check if position (x, y) is out of bounds of patch.
    def _out_bounds(self, x, y):
        return x < 0 or x > self._patchSize or y < 0 or y > self._patchSize

    ## Check if dose time is not within EB machine limit.
    def _out_dose(self, doseTime):
        return doseTime < self._doseTimeMin or doseTime > self._doseTimeMax

    ## Draw straight line
    #
    # @param startX Start x (nm)
    # @param startY Start y (nm)
    # @param endX End x (nm)
    # @param endY End y (nm)
    # @param doseTime Dose time per unit length (μsec.)
    def drawLine(self, startX, startY, endX, endY, doseTime):
        # Round all coordinates to units of 10 nm
        sX = round(startX / self._unit) * self._unit
        sY = round(startY / self._unit) * self._unit
        eX = round(endX / self._unit) * self._unit
        eY = round(endY / self._unit) * self._unit
        # Line should not have same start and end position
        if (
            self._out_dose(doseTime)
            or self._out_bounds(sX, sY)
            or self._out_bounds(eX, eY)
            or ((sX == eX) and (sY == eY))
        ):
            self._errorCount += 1
        else:
            self._commandCount += 1

            # Draw line in CC6
            self._cc6File.write(
                "DWLL(%d,%d,%d,%d,%.1f) ;3\r\n"
                % (
                    (sX / self._unit),
                    (self._patchSize - sY) / self._unit,
                    eX / self._unit,
                    (self._patchSize - eY) / self._unit,
                    doseTime,
                )
            )
            # Draw line in dxf
            self._drawing.add(dxf.line((sX, sY), (eX, eY), color=7))

    def drawlineSquare(self, startX, startY, endX, endY, doseTime):
        # Round all coordinates to units of 10 nm
        sX = round(startX / self._unit) * self._unit
        sY = round(startY / self._unit) * self._unit
        eX = round(endX / self._unit) * self._unit
        eY = round(endY / self._unit) * self._unit
        # 座標がいずれか領域外または
        # x/yのどれか被った場合
        # エラーとみなす
        if (
            self._out_dose(doseTime)
            or self._out_bounds(sX, sY)
            or self._out_bounds(eX, eY)
            or ((sX == eX) or (sY == eY))
        ):
            self._errorCount += 1
        else:
            self._commandCount += 1
            # Ensure sX is on left side
            if sX > eX:
                sX, eX = eX, sX
            # Ensure sY is on top side
            if eY > sY:
                sY, eY = eY, sY

            # Draw rectangle in CC6
            self._cc6File.write(
                "DWLL(%d,%d,%d,%d,%.1f) ;3\r\n"
                % (
                    (sX / self._unit),
                    (self._patchSize - sY) / self._unit,
                    eX / self._unit,
                    (self._patchSize - sY) / self._unit,
                    doseTime,
                )
            )
            self._cc6File.write(
                "DWLL(%d,%d,%d,%d,%.1f) ;3\r\n"
                % (
                    (sX / self._unit),
                    (self._patchSize - eY) / self._unit,
                    eX / self._unit,
                    (self._patchSize - eY) / self._unit,
                    doseTime,
                )
            )
            self._cc6File.write(
                "DWLL(%d,%d,%d,%d,%.1f) ;3\r\n"
                % (
                    (sX / self._unit),
                    (self._patchSize - sY) / self._unit,
                    sX / self._unit,
                    (self._patchSize - eY) / self._unit,
                    doseTime,
                )
            )
            self._cc6File.write(
                "DWLL(%d,%d,%d,%d,%.1f) ;3\r\n"
                % (
                    (eX / self._unit),
                    (self._patchSize - sY) / self._unit,
                    eX / self._unit,
                    (self._patchSize - eY) / self._unit,
                    doseTime,
                )
            )

            # Draw rectange in dxf
            self._drawing.add(dxf.line((sX, sY), (eX, sY), color=7))
            self._drawing.add(dxf.line((sX, eY), (eX, eY), color=7))
            self._drawing.add(dxf.line((sX, sY), (sX, eY), color=7))
            self._drawing.add(dxf.line((eX, sY), (eX, eY), color=7))
            # polyline = dxf.polyline()
            # polyline.add_vertices([(sX, sY), (eX, sY), (eX, eY), (sX, eY), (sX, sY)])
            # self._drawing.add(polyline)

    ## Draw rectangle
    #
    # @param startX Start x (nm)
    # @param startY Start y (nm)
    # @param endX End x (nm)
    # @param endY End y (nm)
    # @param doseTime Dose time (μsec.)
    def drawSquare(self, startX, startY, endX, endY, doseTime):
        # Round all coordinates to units of 10 nm
        sX = round(startX / self._unit) * self._unit
        sY = round(startY / self._unit) * self._unit
        eX = round(endX / self._unit) * self._unit
        eY = round(endY / self._unit) * self._unit
        # 座標がいずれか領域外または
        # x/yのどれか被った場合
        # エラーとみなす
        if (
            self._out_dose(doseTime)
            or self._out_bounds(sX, sY)
            or self._out_bounds(eX, eY)
            or ((sX == eX) or (sY == eY))
        ):
            self._errorCount += 1
        else:
            self._commandCount += 1
            # Ensure sX is on left side
            if sX > eX:
                sX, eX = eX, sX
            # Ensure sY is on top side
            if eY > sY:
                sY, eY = eY, sY

            # Draw rectangle in CC6
            self._cc6File.write(
                "DWSL(%d,%d,%d,%d,%d,%.1f) ;3\r\n"
                % (
                    (sX / self._unit),
                    (self._patchSize - sY) / self._unit,
                    eX / self._unit,
                    (self._patchSize - eY) / self._unit,
                    1,
                    doseTime,
                )
            )

            # Draw rectange in dxf
            polyline = dxf.polyline()
            polyline.add_vertices([(sX, sY), (eX, sY), (eX, eY), (sX, eY), (sX, sY)])
            self._drawing.add(polyline)

    ## Draw single spot
    #
    # @param pX Position x (nm)
    # @param pY Position y (nm)
    # @param doseTime Dose time (μsec.)
    def drawSpot(self, pX, pY, doseTime):
        aX = round(pX / self._unit) * self._unit
        aY = round(pY / self._unit) * self._unit
        # Error check
        if self._out_dose(doseTime) or self._out_bounds(aX, aY):
            self._errorCount += 1
        else:
            self._commandCount += 1
            # Draw spot in CC6
            self._cc6File.write(
                "DWSPS(%d,%d,10,%.1f) ;2\r\n"
                % ((aX / self._unit), (aY / self._unit), doseTime)
            )

            # In DXF, draw as circle with cross mark
            circle = dxf.circle(5, (aX, aY))
            line_h = dxf.line((aX - 5, aY), (aX + 5, aY))
            line_v = dxf.line((aX, aY - 5), (aX, aY + 5))
            for item in (circle, line_h, line_v):
                self._drawing.add(item)

    ## Draw chip marker (four thick lines on each side)
    #
    # @param width Marker width (nm)
    # @param doseTime Dose time (μsec.)
    def drawChipMarker(self, width=3000, doseTime=4.0):
        # Left
        self.drawSquare(0, width, width, self._patchSize - width, doseTime)
        # Right
        self.drawSquare(
            self._patchSize - width,
            width,
            self._patchSize,
            self._patchSize - width,
            doseTime,
        )
        # Top
        self.drawSquare(
            width,
            self._patchSize - width,
            self._patchSize - width,
            self._patchSize,
            doseTime,
        )
        # Bottom
        self.drawSquare(width, 0, self._patchSize - width, width, doseTime)

    ## Draw 10 bit marker assignment
    #
    # @param x The x number of marker
    # @param y The y number of marker
    # @param centerX Marker position x (nm)
    # @param centerY Marker position y (nm)
    # @param doseTime Dose time (μsec.)
    # @param size Width of lines in marker (nm)
    def draw10BitMarker(self, x, y, centerX, centerY, doseTime=1.0, size=1400):
        width = size / 7.0
        # Fix bit
        self.drawSquare(
            -2.5 * width + centerX,
            2.5 * width + centerY,
            -0.5 * width + centerX,
            3.5 * width + centerY,
            doseTime,
        )
        self.drawSquare(
            0.5 * width + centerX,
            2.5 * width + centerY,
            2.5 * width + centerX,
            3.5 * width + centerY,
            doseTime,
        )

        # x(1)
        if x & 1 == 1:
            self.drawSquare(
                -3.5 * width + centerX,
                0.5 * width + centerY,
                -2.5 * width + centerX,
                2.5 * width + centerY,
                doseTime,
            )

        # x(2)
        if x & 2 == 2:
            self.drawSquare(
                -2.5 * width + centerX,
                -0.5 * width + centerY,
                -0.5 * width + centerX,
                0.5 * width + centerY,
                doseTime,
            )
        # x(4)
        if x & 4 == 4:
            self.drawSquare(
                -0.5 * width + centerX,
                0.5 * width + centerY,
                0.5 * width + centerX,
                2.5 * width + centerY,
                doseTime,
            )

        # x(8)
        if x & 8 == 8:
            self.drawSquare(
                0.5 * width + centerX,
                -0.5 * width + centerY,
                2.5 * width + centerX,
                0.5 * width + centerY,
                doseTime,
            )

        # x(16)
        if x & 16 == 16:
            self.drawSquare(
                2.5 * width + centerX,
                0.5 * width + centerY,
                3.5 * width + centerX,
                2.5 * width + centerY,
                doseTime,
            )

        # y(1)
        if y & 1 == 1:
            self.drawSquare(
                -3.5 * width + centerX,
                -2.5 * width + centerY,
                -2.5 * width + centerX,
                -0.5 * width + centerY,
                doseTime,
            )

        # y(2)
        if y & 2 == 2:
            self.drawSquare(
                -2.5 * width + centerX,
                -3.5 * width + centerY,
                -0.5 * width + centerX,
                -2.5 * width + centerY,
                doseTime,
            )
        # y(4)
        if y & 4 == 4:
            self.drawSquare(
                -0.5 * width + centerX,
                -2.5 * width + centerY,
                0.5 * width + centerX,
                -0.5 * width + centerY,
                doseTime,
            )

        # y(8)
        if y & 8 == 8:
            self.drawSquare(
                0.5 * width + centerX,
                -3.5 * width + centerY,
                2.5 * width + centerX,
                -2.5 * width + centerY,
                doseTime,
            )

        # y(16)
        if y & 16 == 16:
            self.drawSquare(
                2.5 * width + centerX,
                -2.5 * width + centerY,
                3.5 * width + centerX,
                -0.5 * width + centerY,
                doseTime,
            )

    def draw10BitLineMarker(self, x, y, centerX, centerY, doseTime=1.0, size=140000):
        width = size / 7.0
        # Fix bit
        self.drawlineSquare(
            -2.5 * width + centerX,
            2.5 * width + centerY,
            -0.5 * width + centerX,
            3.5 * width + centerY,
            doseTime,
        )
        self.drawlineSquare(
            0.5 * width + centerX,
            2.5 * width + centerY,
            2.5 * width + centerX,
            3.5 * width + centerY,
            doseTime,
        )

        # x(1)
        if x & 1 == 1:
            self.drawlineSquare(
                -3.5 * width + centerX,
                0.5 * width + centerY,
                -2.5 * width + centerX,
                2.5 * width + centerY,
                doseTime,
            )

        # x(2)
        if x & 2 == 2:
            self.drawlineSquare(
                -2.5 * width + centerX,
                -0.5 * width + centerY,
                -0.5 * width + centerX,
                0.5 * width + centerY,
                doseTime,
            )
        # x(4)
        if x & 4 == 4:
            self.drawlineSquare(
                -0.5 * width + centerX,
                0.5 * width + centerY,
                0.5 * width + centerX,
                2.5 * width + centerY,
                doseTime,
            )

        # x(8)
        if x & 8 == 8:
            self.drawlineSquare(
                0.5 * width + centerX,
                -0.5 * width + centerY,
                2.5 * width + centerX,
                0.5 * width + centerY,
                doseTime,
            )

        # x(16)
        if x & 16 == 16:
            self.drawlineSquare(
                2.5 * width + centerX,
                0.5 * width + centerY,
                3.5 * width + centerX,
                2.5 * width + centerY,
                doseTime,
            )

        # y(1)
        if y & 1 == 1:
            self.drawlineSquare(
                -3.5 * width + centerX,
                -2.5 * width + centerY,
                -2.5 * width + centerX,
                -0.5 * width + centerY,
                doseTime,
            )

        # y(2)
        if y & 2 == 2:
            self.drawlineSquare(
                -2.5 * width + centerX,
                -3.5 * width + centerY,
                -0.5 * width + centerX,
                -2.5 * width + centerY,
                doseTime,
            )
        # y(4)
        if y & 4 == 4:
            self.drawlineSquare(
                -0.5 * width + centerX,
                -2.5 * width + centerY,
                0.5 * width + centerX,
                -0.5 * width + centerY,
                doseTime,
            )

        # y(8)
        if y & 8 == 8:
            self.drawlineSquare(
                0.5 * width + centerX,
                -3.5 * width + centerY,
                2.5 * width + centerX,
                -2.5 * width + centerY,
                doseTime,
            )

        # y(16)
        if y & 16 == 16:
            self.drawlineSquare(
                2.5 * width + centerX,
                -2.5 * width + centerY,
                3.5 * width + centerX,
                -0.5 * width + centerY,
                doseTime,
            )

    ## Create patterns in two levels.
    #
    # This function will call myShape for each pattern.
    # Level 2 patterns have 10 bit markers.
    # @param lv1xnum Level 1 x count
    # @param lv1ynum Level 1 y count
    # @param lv2xnum Level 2 x count
    # @param lv2ynum Level 2 y count
    # @param lv1width Width of level 1 (nm)
    # @param lv1height Height of level 1 (nm)
    # @param size10BitMarker Width of 10 bit marker line (nm)
    def createPatterns(
        self,
        lv1xnum,
        lv1ynum,
        lv2xnum,
        lv2ynum,
        lv1width,
        lv1height,
        dose_time=3.0,
        size10BitMarker=1400,
    ):
        # Calculate level 2 size
        lv2width = size10BitMarker * 2.0 + lv1width * (lv1xnum)
        lv2height = size10BitMarker * 2.0 + lv1height * (lv1ynum)

        # Total Size
        totalWidth = lv2width * lv2xnum
        totalHeight = lv2height * lv2ynum

        # Initial position of level 2
        lv2inix = (self._patchSize - totalWidth) / 2.0
        lv2iniy = (self._patchSize - totalHeight) / 2.0

        for lv2y in range(lv2ynum):
            for lv2x in range(lv2xnum):
                lv1inix = lv2inix + lv2x * lv2width + size10BitMarker * 2.0
                lv1iniy = lv2iniy + lv2y * lv2height
                for lv1y in range(lv1ynum):
                    for lv1x in range(lv1xnum):
                        cx = lv1inix + lv1width * (lv1x + 0.5)
                        cy = lv1iniy + lv1height * (lv1y + 0.5)
                        self.myShape(cx, cy, lv1x, lv1y, lv2x, lv2y)

                self.draw10BitMarker(
                    lv2x,
                    lv2y,
                    lv1inix - size10BitMarker,
                    lv1iniy + size10BitMarker + lv1ynum * lv1height,
                    dose_time,
                    size=size10BitMarker,
                )

    ## Create patterns for MOKE sample
    #
    # This function will call myShape for each pattern.
    # @param lv1width Width of level 1 (nm)
    # @param lv1height Height of level 1 (nm)
    def createMOKEpattern(self, lv1width, lv1height):
        lv1xnum = int(self._patchSize / lv1width)
        lv1ynum = int(self._patchSize / lv1height)
        self.createPatterns(
            lv1xnum, lv1ynum, 1, 1, lv1width, lv1height, size10BitMarker=0
        )

    ## Set number of dots in one pattern
    #
    # @param dotNum Number of dots
    def setDotNum(self, dotNum):
        self._dotData = np.zeros((dotNum, 7))

    ## Set the offset of reference dot
    #
    # Usually not needed.
    # Sometimes when there is rounding error, this can be useful.
    # @param refNum Number of reference dot
    # @param cx Offset x / nm
    # @param cy Offset y / nm
    def setOrigin(self, refNum, cx, cy):
        self._dotData[refNum, 0] = cx
        self._dotData[refNum, 1] = cy

    ## Set a dot with offset from a reference dot.
    #
    # @param refNum Number of reference dotF
    # @param offset Offset of center position (nm)
    # @param offsetAngle Angle of center position from x-axis (deg.)
    # @param dotLength Length of dot (nm)
    # @param dotAngle Angle of dot (deg.)
    # @param doseTime Dose time (usec.)
    def setDot(
        self, 
        refNum, #dotの番号。この番号を基準にして、他のdotを配置する
        targetNum, #新しく配置するdotの番号
        offset, #参照ドットから新しいドットの中心位置までの距離
        offsetAngle, #参照ドットから新しいドットの中心位置までの角度
        dotLength, 
        dotAngle, #新しく配置するドットの角度
        doseTime
    ):
        cx = offset * np.cos(offsetAngle / 180.0 * np.pi)
        cy = offset * np.sin(offsetAngle / 180.0 * np.pi)
        lx = -dotLength * 0.5 * np.cos(dotAngle / 180.0 * np.pi)
        ly = -dotLength * 0.5 * np.sin(dotAngle / 180.0 * np.pi)
        ox = self._dotData[refNum, 0]
        oy = self._dotData[refNum, 1]
        self._dotData[targetNum, 0] = ox + cx  # origin x
        self._dotData[targetNum, 1] = oy + cy  # origin y
        self._dotData[targetNum, 2] = ox + cx + lx  # x1
        self._dotData[targetNum, 3] = oy + cy + ly  # y1
        self._dotData[targetNum, 4] = ox + cx - lx  # x2
        self._dotData[targetNum, 5] = oy + cy - ly  # y2
        self._dotData[targetNum, 6] = doseTime  # dose time

    ## Draw all dots defined by setDotNum and setDot
    #
    # @param cx Center x
    # @param cy Center y
    def drawDot(self, cx, cy):
        for i in range(len(self._dotData)):
            self.drawLine(
                self._dotData[i, 2] + cx,
                self._dotData[i, 3] + cy,
                self._dotData[i, 4] + cx,
                self._dotData[i, 5] + cy,
                self._dotData[i, 6],
            )

    ## Stigma checker pattern
    #
    # @param centerX Center position x (nm)
    # @param centerY Center position y (nm)
    # @param centerDist Distance of starting position of lines from center (nm)
    # @param length Length of lines (nm)
    # @param doseTime Dose time (μsec.)
    # @param angleLineNum Number of lines in full circle
    def stigmaChecker(
        self,
        centerX=20000,
        centerY=18000,
        centerDist=2000,
        length=1000,
        doseTime=40.0,
        angleLineNum=8,
    ):
        angleUnit = 2 * np.pi / angleLineNum
        for i in range(angleLineNum):
            x1 = centerX + centerDist * np.cos(angleUnit * i)
            y1 = centerY + centerDist * np.sin(angleUnit * i)
            x2 = centerX + (centerDist + length) * np.cos(angleUnit * i)
            y2 = centerY + (centerDist + length) * np.sin(angleUnit * i)
            self.drawLine(x1, y1, x2, y2, doseTime)

    ## Placeholder function for use in createPatterns
    def myShape(self, cx, cy, lv1x, lv1y, lv2x, lv2y):
        Nbit = 8 #bit数,下のiと数を合わせる必要がある
        dose = 50 #最初のdose
        dis = 90 #dot間距離
        length = 65 + 5 * lv1y #データdotとバッファdot長さ

        p = 4 #最初のdotの角度
        D = 1.4 
        pdb = 80 + 2 * lv2x  #datadotのoffsetangleを-90からどれくらい起こすか
        pbd = 4 + 2 * lv2y #bufferdotのoffsetangleを-90からどれくらい起こすか

        db = -(90 - pdb) #datadotのoffsetangle
        bd = -(90 - pbd) #bufferdotのoffsetangle
        dp = -p #datadotの角度
        bp = -(90 - p) #bufferdotの角度

        # Fix dot　最初のdot
        Fset = 200
        Flen = 160
        Fdose = dose + 2 * lv1x
        Foffset = Flen + dis
        # Foffset = Flen + Flen / 2 * (D - 1)
        print(Fdose)

        # Data dot どっち?
        Dset = 100
        Dlen = length #+ 5*lv2x #lv2xごとにdot長さを5あげる
        Ddose = dose + 2 * lv1x
        # Doffset = Dlen * np.cos(22.5 * np.pi / 180) + 10 + 5 * lv1x
        # Doffset = Dlen * D + 5 * lv2x
        Doffset = Dlen + dis

        # BufferDot どっち？
        Bset = 100
        Blen = length #+ 5*lv2x #lv2xごとにdot長さを5あげる
        Bdose = dose + 2 * lv1x
        #Boffset = Blen * D
        Boffset = Blen + dis

        # 描画
        self.setDotNum(2 + Nbit * 2)
        self.setOrigin(0, 0, 0) #原点?
        self.setDot(0, 0, 0, 0, Flen, dp, Fdose)
        self.setDot(0, 1, Foffset * 0.5 + Doffset * 0.5, db + 3, Dlen, bp, Ddose)
        for i in range(8): #Nbitの回数for,上のNbitと同じ数である必要がある
            self.setDot(
                1 + i * 2, 2 + i * 2, Doffset * 0.5 + Boffset * 0.5, bd, Blen, dp, Bdose #bufferdotについて
            )
            self.setDot( #datadotについて
                2 + i * 2, #refnum
                3 + i * 2, #targetnum
                Boffset * 0.5 + Doffset * 0.5, #offset
                db, #offsetangle
                Dlen, #dotlength
                bp, #dotangle
                Ddose, 
            )
            # self.setDot(2, 3, Boffset, 0, Blen, 0, Bdose)
        # self.setDot(3, 4, Boffset, 0, Blen, 0, Bdose)

        self.drawDot(cx, cy)


def main():
    cc6 = CC6Writer()
    cc6.open("d250828hs") #ここにファイル名を入れる
    cc6.createPatterns( #同じ形状のものを作る,createpatternsの変数を変えると描画する数が変わる #lv1width,hightはl1内でのオブジェクトの間隔
        10,
        10,
        5,
        5,
        5000,
        5000,
        1.0,
        1400,
    )
    cc6.drawChipMarker(doseTime=0.5)
    cc6.close()


if __name__ == "__main__":
    main()
