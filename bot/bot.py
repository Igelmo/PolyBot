from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

if __package__ is None or not __package__:
    from sys import path
    path.append('..')

from cl.Expr import compileLine
from cl.TreeVisitor import TreeVisitor


def start(update, context):
    user = update.effective_chat.first_name
    botName = context.bot.username
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello " + user + "! I'm the " + botName + "\nWhat can I do for you?")


def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="This bot has been created as a practice for a faculty subject.")


def myHelp(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Are you lost?\nYou can use different commands in order to comunicate with the bot. You can read more info using the /helpCommands command. The points you provide can be two pairs of real numbers. They have to be always separated by a space. The polygons introduced have to be an array of points as described above separated by two spaces and the array inside a [], for example [0 0  2 0  1 0]. You can check info about the bot using the /info command.")


def helpCommands(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Here you have a list of commands you can use:\n - assignment: we can use ':=' to assign a polygon to a variable. \n - print: prints a polygon. \n - area: calculates and prints the area of a polygon. \n - perimeter: calculates and prints the perimeter of a polygon. \n - area: calculates and prints the area of a polygon \n - vertices: calculates and prints the number of vertices of a polygon.\n - centroid: calculates and prints the centroid of a polygon. \n - color: assign a color to a polygon assigned to a variable. \n - inside: tells if the first polygon is inside the second polygon. \n - equal: tells if both polygons are equal. \n - draw: generate an image with all the polygons indicated. \n - comment: You can write a comment using the // followed by your comment. \n - intersection: You can generate the resulting polygon of the intersection of two polygons using '*'. \n - union: You can generate the resulting polygon of the union of two polygons using '+'. \n - boundingbox: You can generate the resulting polygon of the bounding box of a polygon using '#'. \n - random: You can generate a polygon with n random points using '!' followed by a natural number. \nFor more info you can use the /command you want to see examples.")


def assignment(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can assign a polygon to a variable using the ':='. For example, if we want to assign a polygon [2 0  2 0  0 0] to a variable named p1, we can write p1 := [2 0  2 0  0 0].")


def color(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can assign a color to a variable using the 'color' command. For example, if we want to indicate that the polygon of a variable p1 has a blue color, we have to write color p1, {0 0 1}. The values of the rgb have to be between 0 and 1, both inclusive.")


def myPrint(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can print a variable or directly a polygon using the 'print' command. For example, if we want to print the polygon assigned to a variable p1, we just have to write print p1. Or if we want to print directly a polygon we can do the same, print [1 0  2 0].")


def area(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can calculate the area of polygon using the 'area' command. For example, if we want to know the polygon area assigned to a variable p1, we just have to write area p1. Or if we want to print directly a polygon we can do the same, area [1 0  2 0].")


def perimeter(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can calculate the perimeter of polygon using the 'perimeter' command. For example, if we want to know the polygon perimeter assigned to a variable p1, we just have to write perimeter p1. Or if we want to print directly a polygon we can do the same, perimeter [1 0  2 0].")


def vertices(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can calculate the vertices of polygon using the 'vertices' command. For example, if we want to know the polygon vertices assigned to a variable p1, we just have to write vertices p1. Or if we want to print directly a polygon we can do the same, vertices [1 0  2 0].")


def centroid(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can calculate the centroid of polygon using the 'centroid' command. For example, if we want to know the polygon centroid assigned to a variable p1, we just have to write centroid p1. Or if we want to print directly a polygon we can do the same, centroid [1 0  2 0].")


def inside(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can check if the first polygon indicated is inside the second one. If it's true, it will return 'yes', otherwise a 'no' will return. Let's say we want to check if p1 is inside p2, we just need to write inside p1, p2. We can also do it without variables, for example inside p1, [1 0  2 0].")


def equal(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can check if both polygons indicated are equal. If it's true, it will return 'yes', otherwise a 'no'. Let's say we want to check if p1 is equal to p2, we just need to write equal p1, p2. for example equal [1 0  2 0], p1.")


def draw(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can generate an image showing the polygons indicated using the 'draw' command. You need to provide a name for the image followed by the .png extension, after that indicate the polygons you want to draw. For example, draw \"threePolygons.png\", p1, [1 0  2 0], p2. A polygon color by default is black, if you want a polygon with a concrete color, you have to assign a color to it first, in order to do that please check the /color command.")


def comment(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can add comments by using the '//' followed by your comment. For example //hello i am a comment!")


def intersection(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can generate the resulting convex polygon of an intersection between two polygons with the '*' symbol. For example p1 * p2 or [0 0  2 1] * p2.")


def union(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can generate the resulting convex polygon of an union between two polygons with the '+' symbol. For example p1 + p2 or [0 0  2 1] + p2.")


def boundingbox(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can generate the resulting convex polygon of the bounding box of a polygon with the '#' symbol, followed by a polygon. For example #p1 or #[0 0  2 1].")


def random(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can generate a polygon with n random points [0, 1] using the '!' symbol, followed by n, where n is a natural number. For example !30.")


def polygon(update, context):
    if 'visitor' not in context.user_data:
        context.user_data['visitor'] = TreeVisitor()
    text = update.message.text
    try:
        (resultText, shouldPrint) = compileLine(context.user_data['visitor'], text)
        if shouldPrint:
            if resultText.strip():
                context.bot.send_message(chat_id=update.effective_chat.id, text=resultText)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="_____")
        elif resultText is not None:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(resultText, 'rb'))
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I cannot understand you...")

TOKEN = ""
try:
    TOKEN = open('token.txt').read().strip()
except:
    TOKEN = open('bot/token.txt').read().strip()


def main():
    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('help', myHelp))
    dispatcher.add_handler(CommandHandler('helpCommands', helpCommands))
    dispatcher.add_handler(CommandHandler('assignment', assignment))
    dispatcher.add_handler(CommandHandler('print', myPrint))
    dispatcher.add_handler(CommandHandler('area', area))
    dispatcher.add_handler(CommandHandler('perimeter', perimeter))
    dispatcher.add_handler(CommandHandler('vertices', vertices))
    dispatcher.add_handler(CommandHandler('centroid', centroid))
    dispatcher.add_handler(CommandHandler('color', color))
    dispatcher.add_handler(CommandHandler('inside', inside))
    dispatcher.add_handler(CommandHandler('equal', equal))
    dispatcher.add_handler(CommandHandler('draw', draw))
    dispatcher.add_handler(CommandHandler('comment', comment))
    dispatcher.add_handler(CommandHandler('intersection', intersection))
    dispatcher.add_handler(CommandHandler('union', union))
    dispatcher.add_handler(CommandHandler('boundingbox', boundingbox))
    dispatcher.add_handler(CommandHandler('random', random))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, polygon))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
