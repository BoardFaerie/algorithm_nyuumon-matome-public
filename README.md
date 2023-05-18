
# アルゴリズム入門のまとめ課題

BoardFaerie

## 概要

opencvなどの画像処理系のライブラリを使わずに、numpyと画像表示用のita(もしくはmatplotlib、画像保存用のPIL.Image)(とデバッグ用のwarningsとtime)ライブラリのみでレンダリングパイプラインとシェーダーを作りました。なおOpenGLやDirect3Dは触ったことがなかったので、かなり標準から外れた部分もあるかと思いますがご了承ください。

また、フォントは M+ FONTS PROJECT による M+ BITMAP FONTS を使用させていただきます。このフォントは自由なライセンスで公開されてます。詳細は[こちら](https://mplus-fonts.osdn.jp/mplus-bitmap-fonts/index.html) 。このフォントを編集してノートブックに埋め込みました。このため、このノートブックを開くか走らせる際は、かなり重くなると思われるので注意してください。

最後に、作ったライブラリを使い、デフォルメした地球をアニメーションしてみました。最終アニメーションはtest.mp4およびtest2.gifです。

標準設定の場合、かなり高性能なデスクトップパソコンで開くのに3秒ほど、実行ボタンを押してから実行されるまで5秒ほど、そしてレンダリング(実行そのもの)に3時間程度かかります。

## 参考にしたウェブサイト(主なものだけ)

[Gabriel Gambetta Computer graphics from scratch](https://www.gabrielgambetta.com/computer-graphics-from-scratch/introduction.html)

[Scratchapixel](https://www.scratchapixel.com/index.php)

(これら以外にもQiitaの記事やStack Overflowの質問と答えなどを多数参考にしています。一応参考にしたウェブサイトはコメントに載せてありますが、多分入れ忘れたものもあります。)

## 目次

- 準備部
  - Imports
  - Settings
  - Util
  - Quaternion
- ラスタライズ部
  - Layer
  - Line2D
  - Rectangle2D
  - Circle2D
  - Triangle2D
  - Curve2D
  - Polygon2D
  - Bezier2D
  - Text2D
  - Color
  - Canvas
- ピクセルシェーダー部
  - AntiAliasing
- ジオメトリーシェーダー部
  - ShaderGeometry
- バーテックスシェーダー部
  - ShaderVertex
- レンダリングパイプライン部
  - RayTracing
  - GraphicsPipeline
- 3D部
  - Material
  - WorldObject
  - Light
  - World
- メイン部
  - Main
  - Animation

## 最終アニメーション

![最終アニメーション](https://github.com/BoardFaerie/algorithm_nyuumon-matome-public/blob/4b0778adba23d7b30a8533fae35791e34b93befd/test2.gif)
