class AntiAliasing:
    """Anti Aliasing"""

    @staticmethod
    def SSAA_grid(img, K:int=2):
        """Supersampling Anti-Aliasing with grid, scale K"""
        # https://en.wikipedia.org/wiki/Supersampling
        # https://stackoverflow.com/questions/42463172/how-to-perform-max-mean-pooling-on-a-2d-array-using-numpy
        M, N, C = img.shape
        assert(M % K == 0)
        assert(N % K == 0)
        return img.reshape(M // K, K, N // K, K, C).mean(axis=(1, 3)).astype('u1')
