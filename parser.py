import sys
import os


from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from os import path

from pythonds.basic import Stack
from pythonds.trees import BinaryTree
import plotly.graph_objs as go
from plotly.offline import  plot

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"GUI.ui"))

def main():
   app = QApplication(sys.argv)
   window = mainapp()
   window.show()
   app.exec() #infinte loop


tree_data = []
shapes = []
expresion_stack = []
brackets = []

class mainapp(QMainWindow,FORM_CLASS):

 def __init__(self,parent=None):
    super(mainapp,self).__init__(parent)
    QMainWindow.__init__(self)
    self.setupUi(self)
    self.Handle_UI()
    self.add_process.clicked.connect(self.handle_segmants)
    self.reset.clicked.connect(self.handle_reset)

 def Handle_UI (self):
    self.setWindowTitle("Parser")
    self.setFixedSize(530,1180)

 def circle(self,id,value,x,y):
     global shapes
     global tree_data
     shape = {
         'type': 'circle',
         'xref': 'x',
         'yref': 'y',
         'x0': x+1,
         'y0': y+1,
         'x1': x-1,
         'y1': y-1,
         'line': {
             'color': 'rgba(50, 171, 96, 1)',
         }
     }
     trace3 = go.Scatter(
         x=[x],
         y=[y],
         mode='text',
         text=id,
         hoverinfo='none',
         textposition='middle center',
         textfont=dict(
             family='sans serif',
             size=18,
             color='#000000'
         )
     )
     trace4 = go.Scatter(
         x=[x],
         y=[y-0.5],
         mode='text',
         text=value,
         hoverinfo='none',
         textposition='middle center',
         textfont=dict(
             family='sans serif',
             size=18,
             color='#000000'
         )
     )

     shapes.append(shape)
     tree_data.append(trace4)
     tree_data.append(trace3)

 def square(self,id,value,x,y):
     global tree_data
     trace = go.Scatter(
         x=[x-1, x+1, x+1, x-1,x-1],
         y=[y+1, y+1, y-1, y-1, y+1],
         mode='text+lines',
         text="",
         hoverinfo='none',
         textposition='top center',
         textfont=dict(
             family='sans serif',
             size=18,
             color='#000000'
         )
     )
     trace1 = go.Scatter(
         x=[x],
         y=[y-0.5],
         mode='text',
         text=value,
         hoverinfo='none',
         textposition='middle center',
         textfont=dict(
             family='sans serif',
             size=14,
             color='#000000'
         )
     )

     trace2 = go.Scatter(
         x=[x],
         y=[y],
         mode='text',
         text=id,
         hoverinfo='none',
         textposition='middle center',
         textfont=dict(
             family='sans serif',
             size=18,
             color='#000000'
         )
     )
     tree_data.append(trace)
     tree_data.append(trace1)
     tree_data.append(trace2)

 def exprision(self,tokens,x,y,bracket = []):
     print(tokens)
     global brackets
     print('x is ',x)
     if len(tokens) == 1 and (tokens[0][1] == 'IDENTIFIER' or tokens[0][1] == 'NUMBER'):
         self.circle(tokens[0][1],tokens[0][0],x,y)
         print('last ',x+4)
         return x+4
     elif len(tokens) == 1 and tokens[0] == ['d','DUMMY']:
         bracket = brackets.pop(0)
         print('nside')
         print(brackets)
         print(bracket)
         x = self.exprision(bracket,x,y,brackets)
         return x
     elif len(tokens) == 1:
         _ = tokens[2][4]


     for token in tokens:
         if token == ['(','OPENBRACKET']:
             ind1 = tokens.index(['(', 'OPENBRACKET'])
             ind2 = tokens.index([')', 'CLOSEDBRACKET'])
             tokens1 = [['d','DUMMY']]
             brackets.append(tokens[ind1+1:ind2])
             tokens2 = tokens[:ind1] + tokens1 + tokens[ind2 + 1:]
             x = self.exprision(tokens2, x, y,brackets)
             return x

     chek = True
     chek2 = True

     for ind,token in enumerate(tokens):
         if token == ['<', 'LESSTHAN'] or token == ['>', 'GREATERTHAN'] or token == ['=', 'EQUAL']:
             chek2 = False
             self.circle(token[1],token[0],x,y)
             self.drow_line(x, x, y - 1, y - 3)
             x1 = self.exprision(tokens[:ind],x,y-4,bracket)
             self.drow_line(x, x1, y - 1, y - 3)
             x = self.exprision(tokens[ind+1:],x1,y-4,bracket)
             return x
     if chek2:
        for ind in range(len(tokens),0,-1):
            if tokens[ind-1] == ['+', 'PLUS'] or tokens[ind-1] == ['-', 'MINUS']:
                chek = False
                self.circle(tokens[ind-1][1], tokens[ind-1][0], x, y)
                self.drow_line(x, x, y - 1, y - 3)
                x1 = self.exprision(tokens[:ind-1], x , y - 4 ,bracket)
                self.drow_line(x, x1, y - 1, y - 3)
                x = self.exprision(tokens[ind:],x1 , y-4,bracket)
                return x
     if chek2 and chek:
         for ind in range(len(tokens), 0, -1):
             if tokens[ind-1] == ['*', 'MULT'] or tokens[ind-1] == ['/', 'DIV']:
                 self.circle(tokens[ind-1][1], tokens[ind-1][0], x, y)
                 self.drow_line(x  , x  ,y -1 ,y- 3)
                 x1 = self.exprision(tokens[:ind-1], x, y - 4,bracket)
                 self.drow_line(x  , x1  ,y -1 ,y- 3)
                 x2 = self.exprision(tokens[ind:], x1 , y - 4,bracket)
                 return x2

 def update_tree(self):

     global tree_data
     global shapes



     layout = go.Layout(
         showlegend = False,
         xaxis=dict(
             autorange=True,
             showgrid=False,
             zeroline=False,
             showline=False,
             ticks='',
             showticklabels=False
         ),
         yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
         ),
         shapes=shapes
     )
     fig = go.Figure(data=tree_data, layout=layout)
     plot(fig, filename="parser.html")

 def drow_line(self,x1,x2,y1,y2):
     global tree_data
     trace = go.Scatter(
         x=[x1, x2],
         y=[y1, y2],
         mode='lines',
         text='',
         hoverinfo='none'
     )
     tree_data.append(trace)

 def parser(self,tokens,x,y):
     if len(tokens) == 0 :
         return x
        #read
     elif tokens[0][1] == "READ":
         if tokens[1][1] == "IDENTIFIER":
            self.square('read', tokens[1][0], x, y)
            if len(tokens) > 3:
                self.drow_line(x + 1, x + 3, y, y)
                x = self.parser(tokens[3:], x + 4, y)
                return x
         else:
             _ = tokens[1][4]
         return x + 4

     elif tokens[0][1]  == "WRITE":
        if tokens[1][1] == "IDENTIFIER":
            self.square('write', '', x, y)
            self.circle(tokens[1][1], tokens[1][0], x, y - 4)
            self.drow_line(x, x, y - 1, y - 3)
            if len(tokens) > 3:
                self.drow_line(x + 1, x + 3, y, y)
                x = self.parser(tokens[3:], x + 4, y)
                return x
        else:
            _ = tokens[1][3]
        return x + 4


     elif tokens[0][1]  == "SEMICOLON":
        x = self.parser(tokens[1:],x,y)
        return x

     elif tokens[0][1]  == "IDENTIFIER":
        self.square('assign', tokens[0][0], x, y)
        self.drow_line(x,x,y-1,y-3)
        ind = tokens.index([";", "SEMICOLON"])
        x1 = self.exprision(tokens[2:ind],x,y-4)
        if len(tokens) > ind+2:
            self.drow_line(x + 1  , x1 - 1 , y, y)
            x = self.parser(tokens[ind+1:], x1 , y)
            return x
        return x1

     elif tokens[0][1] == "IF":



         counter = 1
         index2 = -1
         for i in range(1,len(tokens)):
             if tokens[i][1] == "IF":
                 counter+=1
             elif tokens[i][1] == "END":
                 counter-=1
             if counter == 0:
                 index2 = i
                 break




         index1 = tokens.index(["then", "THEN"])
         self.square('if', '', x, y)
         self.drow_line(x, x, y - 1, y - 3)
         x2 = self.exprision(tokens[1:index1],x,y-4)
         self.drow_line(x, x2, y - 1, y - 3)
         x1 = self.parser(tokens[index1+1:index2],x2,y-4)
         if len(tokens) > index2+1:
            self.drow_line(x+1,x1-1,y,y)
            x2 = self.parser(tokens[index2+1:],x1,y)
            print('if ok')
            return x2
         else:
            print('if ok')
            return x1

     elif tokens[0][1] == "REPEAT":
         print('repeat')

         counter = 1
         index1 = -1
         for i in range(1, len(tokens)):
             if tokens[i][1] == "REPEAT":
                 counter += 1
             elif tokens[i][1] == "UNTIL":
                 counter -= 1
             if counter == 0:
                 index1 = i
                 break

         index2 = tokens[index1:].index([";", "SEMICOLON"])
         print(index1,index2)
         self.square('repeat', '', x, y)
         self.drow_line(x, x, y - 1, y - 3)
         x_new = self.parser(tokens[1:index1], x, y - 4)
         print(tokens[index1+1:index1 + index2])
         x2 = self.exprision(tokens[index1+1:index1 + index2],x_new,y-4,[])
         self.drow_line(x , x_new, y - 1, y - 3)

         if len(tokens) > index1 + index2 + 2:
            print("wrong n ")
            self.drow_line(x+1,x2+8-1,y,y)
            x1 = self.parser(tokens[index1 + index2+1:],x2 + 8,y)
            print('repeat ok')
            return x1
         else:
            print('repeat ok')
            return x2

 def handle_reset(self):
     global tree_data
     global shapes

     self.tokens.clear()
     tree_data = []
     shapes = []

 def handle_segmants(self):
     tokens = []
     draw = True
     segmants = self.tokens.toPlainText()
     lines = segmants.split('\n')
     try:
         for line in lines:
             newine = line.replace(","," ")
             words = newine.split()
             tokens.append( words )
         tokens = [x for x in tokens if x != []]
         x = 0
         y = 100
         self.parser(tokens, x, y)


     except:
         QMessageBox.about(self, "Warning", "      enter valid tokens .    ")
         draw = False

     if draw:
         self.update_tree()

if __name__ == '__main__':
   main()