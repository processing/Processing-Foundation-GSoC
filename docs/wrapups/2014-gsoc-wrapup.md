---
title: "Google Summer of Code 2014"
year: 2014
source_url: "https://processingfoundation.org/advocacy/google-summer-of-code/2014"
published: "2014"
archived: "2026-03-09"
---

# Google Summer of Code 2014

  

Original Report: [GSoC 2014](http://shiffman.net/2014/11/01/gsoc-2014/)

**[Android Mode for Processing 3.0](https://github.com/processing/processing-android) by [Imil Ziyaztdinov](https://github.com/imilka/), mentored by [Andres Colubri](https://codeanticode.wordpress.com/)**

The new android mode in Processing 3.0 implements several pieces of functionality that were missing from earlier versions: Export Signed Package (with transparent handling of keystores), device selector, automatic SDK download/installation, and target SDK selector. It also fixed some critical bugs, most notably the missing javac error during package building.

**[Contributions Manager: Reloaded](https://joelmoniz.com/gsoc-2014/) by [Joel Moniz](https://joelmoniz.com/), mentored by [Florian Jenett](http://www.florianjenett.de/)**

The Contributions Manager enables easy and convenient installation, removal, and update of contributions (Libraries, Tools, and Modes) from within the PDE. This summer saw the introduction of a few new features to the Contributions Manager, such as the addition, removal, and update of Tools and Modes without a restart, a new “examples-package”-type contribution, and highlighting contributions. ([source code](https://github.com/processing/processing/commits/master?author=joelmoniz))

**Loom by Chris Johnson-Roberson, mentored by R. Luke DuBois**

Loom lets you create and manipulate patterns of timed events. These patterns can be mapped to audiovisual output, transformed in various ways, and recorded to enable non-realtime synthesis and synchronized video. ([source code](https://github.com/corajr/loom))

**[New video library using GStreamer 1.x](https://github.com/octachoron/gir2java) by [Roland Elek](https://github.com/octachoron), co-mentored by [Levente Farkas](http://lfarkas.org/) and [Andres Colubri](https://codeanticode.wordpress.com/)**

The aim of this project was to create a set of Java bindings for the GStreamer 1.x series, automatically generating everything where applicable, and then updating the video library in Processing to use these new bindings. We were able to solve the most challenging problem — the automatic generation of Java code directly from the GObject Introspection data — using a library called CodeModel, and BridJ as the native interoperability library. In addition to this, we modified the current Java bindings in order to run the video library with the latest stable release of the gstreamer toolkit (1.4.0), which confirms that the new gstreamer binaries (released for Windows and Mac OSX plarforms by the gstreamer organization itself) can be successfully loaded from Processing. At the time of conclusion of GSOC, the new bindings were still not ready to use as the basis of the new video library, however we are very confident that we will achieve the final goal within the next two months.

**[ofSketch](https://github.com/olab-io/ofSketch) by [Brannon Dorsey](http://brannondorsey.com/), mentored by [Christopher Baker](http://christopherbaker.net/)**

ofSketch is a barebones browser-based IDE for [openFrameworks](http://openframeworks.cc/). Targeted toward new users, ofSketch decreases the openFrameworks barrier to entry by providing a “plug and play” development environment that allows users to spend more time coding and less time with configuration. In addition to its simplicity, ofSketch supports powerful extended functionality like API specific autocomplete, compilation feedback, error reporting, project export, remote coding capabilities, and Raspberry Pi support to fit the needs of intermediate coders.

**[p5.sound](http://p5js.org/reference/#/libraries/p5.sound) by [Jason Sigal](http://www.jasonsigal.cc/), mentored by [Evelyn Eastmond](http://www.evelyneastmond.com/), is an addon for p5.js**

p5.sound brings the Processing approach to Web Audio. Its functionality includes audio input, playback, manipulation, effects, recording, analysis, and synthesis with syntax built off of Wilm Thoben’s Sound for Processing library. The project is on [GitHub](https://github.com/processing/p5.js-sound), with interactive documentation and learning examples on [p5js.org](http://p5js.org/). This summer, Jason also wrote methods for file input / output and ported Processing’s Table / TableRow classes to p5.

**[p5 IDE](https://github.com/processing/p5.js-editor) by [Sam Lavigne](http://lav.io/), mentored by Lauren McCarthy**

An easy to use desktop IDE for creating p5.js projects.

**[PDE X for Processing 3.0](http://www.mkmoharana.com/2014/08/google-summer-of-code-2014-its-wrap.html) by [Manindra Moharana](http://www.mkmoharana.com/), mentored by Daniel Shiffman**

PDE X is a Processing mode that introduces advanced IDE features like code completion, refactoring, live error checking, debugger and more. The goal of the project was to bring PDE X to a stable state and make it the default editor for Processing 3.0. The main focus was on fixing the last remaining bugs and tweaking/refining what was already present. A few new features were also introduced. Please see [Manindra’s post](http://www.mkmoharana.com/2014/08/google-summer-of-code-2014-its-wrap.html) for more details on what was accomplished. ([source code](https://github.com/processing/processing/commits/master?author=Manindra29))

**[POculus](https://github.com/pratik9891/ProcessingOculus) by [Pratik Sharma](https://pratikgsoc.wordpress.com/), mentored by Elie Zananiri**

POculus provides an Oculus renderer for Processing. Any P3D sketch can be made Oculus ready by using the POculus renderer. ([source code](https://github.com/pratik9891/ProcessingOculus))

**Sound for Processing 3.0 by [Wilm Thoben](http://www.wilmthoben.com/), mentored by Casey Reas**

Sound is the new core lightweight sound library for Processing. The project started in late 2013 and in GSoC 2014 new features, bug fixes, and cross platform support were introduced. Sound uses a customized and enhanced version of methcla, a C++ sound engine. The native bindings allow for low latency support which is a new feature. Sound is a collection of sound-synthesis objects, analyzers, and effects.

**[TweakMode for Processing 3.0](http://www.galsasson.com/tweakmode/) by [Gal Sasson](http://www.galsasson.com/), mentored by Daniel Shiffman**

Tweak is a new execution mode in Processing 3.0 that allows changing sketch parameters in realtime. TweakMode was created last year in GSoC 2013 as a separate mode, and was brought into Processing 3.0 this summer, with some modifications and fixes. ([source code](https://github.com/processing/processing/commits/master?author=galsasson))

---

*Originally published on [processingfoundation.org](https://processingfoundation.org/advocacy/google-summer-of-code/2014). Archived 2026-03-09.*
