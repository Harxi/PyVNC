class PixelFormat:
    def __init__(self, bitsPerPixels: int, depth: int, bigEndianFlag: bool, trueColorFlag: bool, RGBMax: tuple[int], RGBShift: tuple[int], padding: tuple[int]):
        self.bitsPerPixels = bitsPerPixels
        self.depth = depth
        self.bigEndianFlag = bigEndianFlag
        self.trueColorFlag = trueColorFlag
        self.RGBMax = RGBMax
        self.RGBShift = RGBShift
        self.padding = padding
