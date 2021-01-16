# https://stackoverflow.com/questions/25333732/matplotlib-animation-not-working-in-ipython-notebook-blank-plot/30845792
# https://ossyaritoori.hatenablog.com/entry/2018/12/01/matplotlib%E3%81%A7%E3%82%A2%E3%83%8B%E3%83%A1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%92%E4%BD%9C%E6%88%90%EF%BC%8C%E4%BF%9D%E5%AD%98

ani = animation.ArtistAnimation(fig, imgs, interval=1000 / Settings.FPS, repeat=True, blit=True)
ani

ani.save("test2.gif", writer='imagemagick')
ani.save('test.mp4', writer="ffmpeg")
