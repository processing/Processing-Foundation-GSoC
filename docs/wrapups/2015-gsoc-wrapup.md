---
title: "Google Summer of Code 2015"
year: 2015
source_url: "https://processingfoundation.org/advocacy/google-summer-of-code/2015"
published: "2015"
archived: "2026-03-09"
---

# Google Summer of Code 2015

  

Original Report: [GSoC 2015](https://github.com/shiffman/GSOC-2015-Report/blob/gh-pages/report.md)

**[p5.js Windows Port](https://github.com/processing/p5.js-editor) by [Guy de Bree](https://github.com/Bruehausu), mentored by [Sam Lavigne](https://github.com/antiboredom)**

For my Google Sumer of Code I developed a Windows port for the p5.js IDE, and fixed bugs for said editor. It’s now on the p5.js website! While it still has bugs, you can try it out on the [downloads page](http://p5js.org/download/). ([source code](https://github.com/processing/p5.js-editor))

**New Kinect libraries openKinect and KinectPV2 by [Thomas Sanchez Lengeling](http://codigogenerativo.com/), mentored by [Elie Zananiri](http://dpt.co/en/home/)**

The goal of the project was to expand and update the existing Kinect libraries; OpenKinect-for-Processing and KinectPV2. The openKinect library now supports the new Kinect v2 for Mac and Windows and Kinect v1 for Windows and Linux. For the KinectPV2, functionalities include: skeleton tracking, face detection, process frame raw data, point cloud extraction and contour extraction. Source sode on github: [OpenKinect-for-Processing](https://github.com/shiffman/OpenKinect-for-Processing) and [KinectPV2](https://github.com/ThomasLengeling/KinectPV2).

**[Processing.py 3.0 Update](https://github.com/Luxapodular/processing.py) by [Luca Damasco](https://github.com/Luxapodular), mentored by [Golan Levin](https://github.com/golanlevin)**

Prior to the start of the Google Summer of Code, Processing’s Python mode would not work at all with Processing 3.0 due to some extensive back-end changes. Fortunately, this summer saw the revitalization and updating of Python Mode! Users may now write Processing 3.0 Sketches using Python syntax in the new editor. Due to a few outstanding bugs, it has not yet been officially released, but feel free to try it out by building the [Processing.py Source](https://github.com/Luxapodular/processing.py) on your own machine. In addition to once again making Python Mode functional, I have edited over 1,000 lines of reference code as well as ported nine new tutorials! [Feel free to check them out and leave feedback!](https://github.com/Luxapodular/processing-py-site)

**[Web IDE for p5.js](https://github.com/therewasaguy/p5js-webIDE) by [Jason Sigal](http://jasonsigal.cc/), mentored by Daniel Shiffman**

A browser-based code editor, designed specifically for the p5.js community. The project adapts the p5.js Desktop IDE (originally by Sam Lavigne, GSOC ’14) for the web, with inspiration/insight from Gene Kogan's p5 Sandbox. The goal is to make it easy to create, browse, share, and remix creative code sketches directly from the browser. Every project gets a unique URL and version control (through GitHub Gists). Logged-in users can access their previous sketches, and all users can access curated p5.js examples. Create an account and start sketching! Demo at [p5ide.herokuapp.com](http://p5ide.herokuapp.com/).

**Raspberry Pi and armv7hf support by [Gottfried Haider](http://gottfriedhaider.com/), mentored by Ben Fry**

Gottfried worked on making Processing play well with the Raspberry Pi and similar ARM-powered microcomputers (to borrow a term used in the 1970s to describe various kits and designs built around affordable microprocessors, such as the Motorola 6800). Initial support got [merged](https://github.com/processing/processing/commits/master?author=gohai) into processing.git in time for Processing 3.0. The upcoming 3.0.1 release will contain all remaining parts, such as the bits necessary for having working OpenGL graphics on the Pi (with some great help by the JOGL team). Part of the work also involved the creation of a new core library, [Hardware I/O](https://processing.org/reference/libraries/io/index.html), that was made to provide access to the hardware peripherals, such as GPIO, I2C and SPI, that are generally made available on pin headers on such systems. The hope was that using those could be as simple and straightforward as it is on the Arduino platform today. To learn more: Notes about running [Processing on ARM Linux](https://github.com/processing/processing/wiki/ARM-Linux) and the [Raspberry Pi & Raspberry Pi 2](https://github.com/processing/processing/wiki/Raspberry-Pi). A short (vertical!) [video clip](https://vimeo.com/131480032) showing the GPIOs in action.

**[p5.SVG](https://github.com/zenozeng/p5.js-svg) and [p5.PDF](https://github.com/zenozeng/p5.js-pdf) by [Zeno Zeng](https://github.com/zenozeng), mentored by [Danne Woo](https://github.com/dannewoo)**

The main goal of p5.SVG is to provide a SVG runtime for p5.js, so that we can draw using p5’s powerful API in svg, save things to svg file and manipulating existing SVG file without rasterization. [Source code on GitHub](https://github.com/zenozeng/p5.js-svg). As for p5.PDF, it’s a simple PDF export module for p5.js based on browser's print to pdf function. ([source code](https://github.com/zenozeng/p5.js-pdf))

**[internationalization of p5.js website](https://github.com/processing/p5.js-website) & [collection of sketches for the p5.js community statement video](https://github.com/mayaman/p5jsCommunitySketches) by [Maya Man](https://github.com/mayaman/), mentored by Johanna Hedva**

This summer, I worked primarily on two separate projects. First, I rebuilt the p5.js (currently built in php) using Node.js, Assemble, Grunt, Handlebars, & YAML to support internationalization (easy tranlations from English to foreign languages // button styling to be adjusted & tranlsations to be completed at upcoming translat-a-thons). Second, I collected and currated sketches contributed from people around the world to play in the background our p5.js community statement video. Check out the projects on my github (source code below)!

[i18n site source code](https://github.com/processing/p5.js-website)

[community sketches source code](https://github.com/mayaman/p5jsCommunitySketches)

**Contribution Manager UI upgrade by [Akarshit Wal](https://github.com/Akarshit), mentored by [Scott Murray](https://github.com/alignedleft)**

Contribution Manager is a tool which lets uers install/upgrade/remove various libraries and other contributions. The aim of the project was to change UI of the Contribution Manager and make it more user-friendly. Another small part of the project was to test all the libraries and their examples to check their compatibility with Processing 3.0 and collect data about what is missing in them.

**[RSyntaxTextArea integration](https://github.com/joelmoniz/processing/tree/RSTA) and [the REPL Mode](https://github.com/joelmoniz/REPLmode) by [Joel Moniz](https://joelmoniz.com/), mentored by [Manindra Moharana](http://www.mkmoharana.com/)**

The RSyntaxTextArea integration aimed at replacing the JEditTextArea, which is currently at the heart of the PDE editor, with the RSyntaxTextArea and the complementary AutoComplete code completion library to bring several new features to the table, such as code folding and documentation support and parameter tabbing during auto-completion. The REPL mode adds a Read-Evaluate-Print-Loop console to processing, enabling users to type in processing code, and to view the output of this code immediately. This mode also gives the PDE the ability to hot swap code, wherein the output corresponding to changes made in a running sketch can be viewed by simply saving the sketch, without restarting it. A detailed report of everything that was undertaken this summer can be found [here](http://joelmoniz.com/gsoc-2015/).

**p5bots by [Sarah Groff-Palermo](http://sarahgp.com/), mentored by Shawn van Every**

p5bots combines a socket layer and a simplified API to enable users to interact with an Arduino (or other microprocessor) from within the browser. Use sensor data to drive a sketch; use a sketch to to affect the real world.

**p5 WebGL Renderer by [Karen Peng](http://karenlabs.com/), mentored by [Kevin Siwoff](http://http//kevinsiwoff.com/)**

A light-weight webGL renderer for p5.js. Over the summer, basic webGL APIs for p5.js are implemented. It enables you to create sketches under WebGL mode, while all the syntaxes remain consistent with p5 2D (default) mode. WebGL APIs includes: cameras, geometries, lights, materials, texture, etc. For more detail, references are [documented](http://p5js.org/reference/). Get started with [p5 webGL tutorial](https://github.com/processing/p5.js/wiki/Getting-started-with-WebGL-in-p5). Take a look at [3D examples](http://p5js.org/examples/).

**[Video and Audio streaming library](https://github.com/nconfrey/GSoC) by Nick Confrey, mentored by Dan Shiffman**

Thanks to [Andres Coulbri](https://github.com/codeanticode/) and [Gottfried Haider](https://github.com/gohai) for their exceptionally helpful code and examples. Thanks also to my mentor Dan Shiffman for direction and help throughout all the weeks. This project is broken up into roughly three useful parts. It originally focused on streaming media over the network, primarily video and audio streams, but evolved to include revamping Processing's video core video framework. I planned to write networking code in Java, but the project evolved to consist of learning and developing C to Java conversion through Java Native Interface and Java Native Access. Along the way I also picked up skills in video codecs, network packet payloading, and audio encoding. The first part of the project was modifications and extensions to the existing Processing network library. The second part was upgrading Processing's video capability to use GStreamer 1.0 instead of the depreciated GStreamer 0.10 which Processing was previously relying. Finally, the Processing community can access the most recent version of GStreamer, and with it, the most recent plugins. While the code itself is highly tailored towards videostreaming and video playback, the same JNI technique can be used to access the wealth of GStreamer resources, from CD ripping all the way to audio analysis. Processing users will now have much more power in the areas of video and audio. I have also left exposed a public static void pipelineLaunch(String pipe) function, which parses a GStreamer pipeline string and then launches and runs the pipeline. The third part of the project was creating a streaming library that allows Processing users to stream local videos and songs/audio files to other sketches and other computers.

---

*Originally published on [processingfoundation.org](https://processingfoundation.org/advocacy/google-summer-of-code/2015). Archived 2026-03-09.*
