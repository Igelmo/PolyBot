


# Python LP project: PolyBot

## Table of contents

[Description](#description)
[Installation](#installation)
[Usage](#usage)
[Credits](#credits)
[License](#license)


## Description
This project consists on implementing a Telegram Bot that replies textually and graphically to operations related to convex polygons.

In order to do this, we created a polygons.py class, that contains all the required and necessary operations. 

A programming language to work with convex polygons, using the functions defined and implemented on the polygons.py file. Using ANTLR with Python.

Finally, a bot.py file that contains the implementation of the Telegram Bot.

## Package structure
If we unzip the file, it will generate the next content:

 - A requirements.txt with the libraries needed to use the project.
 - This README.md
 - a file named polygons.py that contains the class ConvexPolygon and all the functions needed for the proper functioning of the project.
 - A package named cl, containing all the compiler parts, we can stand out three files:
     - A Expr.py file that contains the compiler script
     - A TreeVisitor.py file, used to read and travel all the tree generated in a compiler command.
     - A Expr.g where we can see the grammar that the compiler expect to find.
- A package named bot, containing the files the telegram bot needs.

## Installation
First of all, we need to install Python, this project is implemented with Python3 so we have to install it by introducing to our terminal the command below:

If you are using Windows or Mac, you simply can access the corresponding store and install it from there.

If you are using Linux, you can install python3 using the following commands:
```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.8
```
After that, we can use the requirements.txt to install all the necessary libraries. We just have to run the next command:
```
python -m pip install -r requirements.txt
```
However, you have next how to install the libraries and all the necessary below. If you didn't have any problem with the requirements.txt and all was successfully installed, just ignore the rest of the installation section.

For the draw functionality used on the polygons.py file, we need to install the pillow library. We can do it by executing the command below, regardless of the OS :

```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

### Compiler
In order to install the ANTLR, we need to run the next command:
```
pip install antlr4-python3-runtime
```
When the installation is finished, we have to configure the classpath. In order to do so, please, follow the next steps defined on the link below:

https://github.com/antlr/antlr4/blob/master/doc/getting-started.md

You will have all the necessary files in the cl package (including the lexer and parser files). However, if there's any problem with them, above are the instructions to generate all the parser and lexer files again:

    Delete all the files on the cl package except the (Expr.py, TreeVisitor.py, Expr.g and \_\_init__.py files). After that, we have to compile the Expr.g in order to generate all the parser and lexer files. To do so, we have to execute the next command on a terminal in the cl directory:
```
antlr4 -Dlanguage=Python3 -no-listener -visitor Expr.g
```

### Telegram Bot
To execute the bot.py in order to activate the polybot, we will need to install the next library:
```
pip3 install python-telegram-bot
```
We have to write pip depending of the system we are using.

## Usage

### Compiler

To use correcly the compiler we can just execute the file Expr.py. In there, we have the compiler script that comunicates with also the ConvexPolygon class.

We can execute the compiler from inside the cl package with the following command:
```
python Expr.py
```
Or from the root directory of the project with the command:
```
python -m cl.Expr
```
Once Expr.py is executed we will see a ? at the terminal. That means the compiler is expecting an input. We can write the following commands:

 - Assign a polygon to a variable:
 We can assign a polygon to a variable with the command `:=` For exemple, we can assign to a variable named p1 the polygon [0 0 &nbsp; 1 0 &nbsp; 2 0 &nbsp; -0.2 0.8] as below:
 

    > p1 := [0 0 &nbsp; 1 0 &nbsp; 2 0 &nbsp; -0.2 0.8]

 - Print:
 The print command outputs the polygon array of points. This function is usefull if we have the need to know the polygon stored on a variable. For example:
    > print p1
    
 - Area:
 We can ask the area of a polygon using this command. We can use it by writing directly a polygon or with a polygon already stored on a variable. As we can se below:

    >  area p1

    >  area  [0 0 &nbsp; 1 0 &nbsp; 2 0 &nbsp; -0.2 0.8]

 - Perimeter:
 As in the area command, we can ask for a polygon's perimeter as below:

    >  perimeter p1

    >  perimeter [0 0 &nbsp; 1 0 &nbsp; 2 0 &nbsp; -0.2 0.8]

 - Vertices:
We can also print the vertices a polygon has:

    > vertices p1

    > vertices  [0 0 &nbsp; 1 0 &nbsp; 2 0 &nbsp; -0.2 0.8]

 - Centroid:
 With the centroid command we can calculate the centroid of a polygon:

    > centroid p1

    > centroid  [0 0 &nbsp; 1 0 &nbsp; 2 0 &nbsp; -0.2 0.8]

 - Color:
 If we want to assign a color to a polygon in order to see the polygon in a different color when drawn. We can use this command. We need to express the color in rgb between {}, as {r g b}. Where r,g and b have to be a float number between 0 and 1 inclusive. For example, if we want to assign a blue color to the polygon assigned to the variable p1, we can do it by writing the next command:

    >  color p1, {0 0 1}
    
 - Inside:
The inside command tells if the first polygon is inside the second polygon. This can be done with variables or polygons directly. For example:

    > inside p1, [0 0 &nbsp; 1 0 &nbsp; 3 0 &nbsp; -0.2 0.8]

    If p1 is inside the polygon [0 0 &nbsp; 1 0 &nbsp; 3 0 &nbsp; -0.2 0.8], it will return "yes", otherwise a "no" will be returned.

 - Equal:
 The equals command tells if two polygons are equal.        This can be done with variables or polygons directly. As we have seen in the inside command too. For example:
    > equal p1, [0 0 &nbsp; 1 0 &nbsp; 3 0 &nbsp; -0.2 0.8]
 
    If p1 is equal to the polygon [0 0 &nbsp; 1 0 &nbsp; 3 0 &nbsp; -0.2 0.8], it will return "yes", otherwise a "no" will be returned.

 - Draw:
 The draw command creates a .png with the polygons indicated drawn in the image. In order to do so, we need to indicate the name of the image we want to generate followed by the polygons we want to draw separated by `,`. For example:

    >  draw "threepolygons.png", p1, [0 0 &nbsp; 1 0 &nbsp; 3 0 &nbsp; -0.2 0.8], p2

    Notice that we write the file name with the extension on it.
 - Comments:
 We can write comments on the commands we write with a `//` followed by our comment. For example:
 
    > // I'm a comment, hi!
    
    We can write a commend after a command too:
    > draw "aPolygonIsAlone.png", p1 // This will draw in the aPolygonIsAlone.png a single polygon!

 - The use of operators:
 We can use also different operations with our polygons, the options are listed below:
     - Intersection:
        We can calculate the resulting intersection of two polygons with the `*` sign:
        > p1 * p2
        
    This will print the resulting convex polygon (the intersection) of the two polygons.
     - Convex Union:
     We can do the same as in the interection operation but with the union, using the `+` sign:
        >  p1 + p2

     - Bounding box of a polygon:
    We can do it using the # sign before the variable or polygon:
        >   #p1
    
    This will print the bounding box of the polygon assigned to the variable p1.
     - Random:
     This function is expressed with the `!` sign will generate a polygon with n random vertices. n has to be a natural number. Below we have an example:
        > !30

    This command will generate a polygon with 30 random vertices
 
In order to exit the compiler we can write `:q`.

### Telegram Bot
In order to use the telegram bot, we must have to install telegram on our mobile device.

After that we can execute the bot.py to execute the telegram bot we can do it inside the bot package with:
```
python bot.py
```
Or in the root package of the project with:
```
python -m bot.bot
```
Once we have the Telegram app installed and the bot running, we can access to t.me/ConvexPolygonLPLaiaBot to start a chat with our bot. The name of the bot is @ConvexPolygonLPLaiaBot.

When we have entered the chat, we can use different commands described below:
 - /start: The bot says hello and welcomes you. Used to see if the bot is responding.
 - /info: Print a brief info about the bot.
 - /help: Print as a bot message how to use the bot, commands and how to introduce a readable input for the bot.
 - /helpCommands: Print all the commands you can use.
 Without introduce a command, we can just use the original commands used and documented in the compiler, as described in the subsection above:
        For example, if we want to print a polygon, say, [0 0  1 0  2 0], we can ask to print the polygon to the bot as:
        ``` print [0 0  1 0  2 0] ```
 
 ### It's important to know that
 In both Compiler and Telegram bot usages:
 - The points introduced can be two pairs of real numbers. They have to be always separated by a space. 
For example 0 0 or 4.2 -2.9
 - The polygons introduced have to be an array of points as described above separated by two spaces and the array inside a []. 
 For example [0 0 &nbsp; 1 0 &nbsp; 2 0 &nbsp; -0.2 0.8]
- If you don't assign any color to a polygon, by default the polygon will be black when drawn
- Notice that if we introduce a non convex polygon, the program automatically will generate the convex hull of the desired polygon.

## Credits:
Laia Igelmo Amorós

## License
MIT License
Copyright (c) [2020] [Laia Igelmo Amorós]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

