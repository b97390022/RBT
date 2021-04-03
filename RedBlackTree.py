import sys
from termcolor import colored
import random
from typing import Any, Callable,Generator, Coroutine, Union
from functools import wraps
import inspect

def typeCheck(func):
  @wraps(func)
  def helper(*args, **kwargs):
    argtype = tuple(func.__annotations__.values())
    
    if len(args) + len(kwargs) -1 > len(argtype):
      raise ValueError('Too much params!')
    if len(args) > 0:
      for i, v in enumerate(args[1:]):
        if hasattr(argtype[i], '__origin__'):
          if argtype[i].__origin__ is Union:
            if not isinstance(v, argtype[i].__args__):
              raise TypeError(f'Wrong type! it must be {argtype[i]}.')
        else:
          if not isinstance(v, argtype[i]):
            raise TypeError(f'Wrong type! it must be {argtype[i]}.')
    if kwargs:
      for i, v in enumerate(kwargs):
        if hasattr(func.__annotations__[v], '__origin__'):
          if func.__annotations__[v].__origin__ is Union:
            if not isinstance(kwargs[v], func.__annotations__[v].__args__):
              raise TypeError(f'Wrong type! it must be {func.__annotations__[v]}.')
        else:
          if not isinstance(kwargs[v], func.__annotations__[v]):
            raise TypeError(f'Wrong type! it must be {func.__annotations__[v]}.')

    return func(*args, **kwargs)
  return helper

ANSI = {
  'RESET':'\u001B[0m',
  'BLACK':'\u001B[30m',
  'RED':'\u001B[31m',
}

class RedBlackTree():
  class Node():
    def __init__(self, value=None, data=None, leftSize=0, parent=None, color = 1):
      self.value = value
      self.data = data
      self.leftSize = leftSize
      self.parent = parent
      self.left = None
      self.right = None
      self.color = color #1 as red, 0 as black
    
    def __str__(self):
      if self.parent != None:
        parent = self.parent.value
      else:
        parent = None
      
      if self.left != None:
        if self.left.value != None:
          left = self.left.value
        else:
          left = None
      else:
        left = None
      
      if self.right != None:
        if self.right.value != None:
          right = self.right.value
        else:
          right = None
      else:
        right = None

      parent_color = self.parent.color if parent is not  None else None
      parent = colored(parent,'red') if parent_color == 1 else (ANSI['BLACK'] + str(parent)) if parent_color == 0 else colored(parent,'magenta')
      self_color = self.color if self is not  None else None
      self_node = colored(self.value,'red') if self_color == 1 else (ANSI['BLACK'] + str(self.value)) if self_color == 0 else colored(self.value,'magenta')
      left_color = self.left.color if left is not None else None
      left = colored(left,'red') if left_color == 1 else (ANSI['BLACK'] + str(left)) if left_color == 0 else colored(left,'magenta')
      right_color = self.right.color if right is not None else None
      right = colored(right,'red') if right_color == 1 else (ANSI['BLACK'] + str(right)) if right_color == 0 else colored(right,'magenta')

      return \
      '''
            {}
            |
            {}
            /  \\
          {}     {}
      '''.format(str(parent),str(self_node),str(left),str(right))

  @typeCheck
  def __init__(self, input:Union[dict, list]=None, randNum:int=0):
    # need NULL node template
    self.NULL = self.Node(color=0)
    self.root = self.NULL
    self.length = 0
    self.red = 0
    self.black = 0

    # construct at init
    if randNum != 0 and input != None:
      raise TypeError('You can only choose one type!')
    elif isinstance(input, dict):
      for i in input:
        self.insert(i, input[i])
    elif isinstance(input, list):
      for i in input:
        self.insert(i, None)
    elif randNum != 0:
      lst = [*range(randNum)]
      random.shuffle(lst)
      for i in lst:
        self.insert(i, None)

  def __len__(self):
    return self.length

  def __eq__(self, obj):
    return self.length == obj.length

  def __lt__(self, obj):
    return self.length < obj.length

  def __le__(self, obj):
    return self.length <= obj.length

  # printing the tree
  def print_tree(self, val="value", left="left", right="right", color='color', getColor=True):
    def __display(root=self.root, val=val, left=left, right=right, color=color, getColor=getColor):
      """Returns list of strings, width, height, and horizontal coordinate of the root."""
      # No child.

      if root == self.NULL or root is None:
        line = '%s' % colored(getattr(root, val),'magenta',attrs=['bold'])
        width = len(line)-13
        height = 1
        middle = width // 2
        return [line], width, height, middle
        

      elif (getattr(root, right) == self.NULL or getattr(root, right) is None) and (getattr(root, left) == self.NULL or getattr(root, left) is None):
        
        left, n, p, x = __display(getattr(root, left))
        right, m, q, y = __display(getattr(root, right))
        
        if not getColor:
          s = '%s' % getattr(root, val)
        else:
          if getattr(root, color) == 1:
            s = '%s' % colored(getattr(root, val),'red',attrs=['bold'])
          else:
            s = '\u001b[30m%s' % colored(getattr(root, val),attrs=['bold'])

        u = len(s)-13
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
          left += [n * ' '] * (q - p)
        elif q < p:
          right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

      # Only left child.
      if getattr(root, right) is None or getattr(root, right) is self.NULL:
        left, n, p, x = __display(getattr(root, left))
        right, m, q, y = __display(getattr(root, right))

        if not getColor:
          s = '%s' % getattr(root, val)
        else:
          if getattr(root, color) == 1:
            s = '%s' % colored(getattr(root, val),'red',attrs=['bold'])
          else:
            s = '\u001b[30m%s' % colored(getattr(root, val),attrs=['bold'])

        u = len(s)-13
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
          left += [n * ' '] * (q - p)
        elif q < p:
          right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

      # Only right child.
      if getattr(root, left) is None or getattr(root, left) is self.NULL:
        left, n, p, x = __display(getattr(root, left))
        right, m, q, y = __display(getattr(root, right))

        if not getColor:
          s = '%s' % getattr(root, val)
        else:
          if getattr(root, color) == 1:
            s = '%s' % colored(getattr(root, val),'red',attrs=['bold'])
          else:
            s = '\u001b[30m%s' % colored(getattr(root, val),attrs=['bold'])

        u = len(s)-13
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
          left += [n * ' '] * (q - p)
        elif q < p:
          right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

      # Two children.
      left, n, p, x = __display(getattr(root, left))
      right, m, q, y = __display(getattr(root, right))

      if not getColor:
        s = '%s' % getattr(root, val)
      else:
        if getattr(root, color) == 1:
          s = '%s' % colored(getattr(root, val),'red',attrs=['bold'])
        else:
          s = '\u001b[30m%s' % colored(getattr(root, val),attrs=['bold'])
          
      u = len(s)-13
      first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
      second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
      if p < q:
        left += [n * ' '] * (q - p)
      elif q < p:
        right += [m * ' '] * (p - q)
      zipped_lines = zip(left, right)
      lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
      return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, *_ = __display(self.root, val, left, right)

    if (RBT.red + RBT.black) == 0:
      print(f'RedNode:{RBT.red}({0:.2%}), BlackNode:{RBT.black}({0:.2%})')
    else:
      print(f'RedNode:{RBT.red}({RBT.red/(RBT.red + RBT.black):.2%}), BlackNode:{RBT.black}({RBT.black/(RBT.red + RBT.black):.2%})')
    for line in lines:
        print(line)

  # V-L-R
  def preOrderPrint(self, node=None):
    node = self.root if node is None else node
    if node != self.NULL:
      sys.stdout.write(str(node.value) + " ")
      self.preOrderPrint(node.left)
      self.preOrderPrint(node.right)

  # L-V-R
  def inOrderPrint(self, node=None):
    node = self.root if node is None else node
    if node != self.NULL:
      self.preOrderPrint(node.left)
      sys.stdout.write(str(node.value) + " ")   
      self.preOrderPrint(node.right)

  # L-R-V
  def postOrderPrint(self, node=None):
    node = self.root if node is None else node
    if node != self.NULL:
      self.preOrderPrint(node.left)
      self.preOrderPrint(node.right)
      sys.stdout.write(str(node.value) + " ")

  # for testing
  def testLeftRotate(self, root:Node = None):
    root = self.root.right if root is None else root
    self.__leftRotate(root)

  # for testing
  def testRightRotate(self, root:Node = None):
    root = self.root.left if root is None else root
    self.__rightRotate(root)

  @typeCheck
  def search(self, value:int, printResult:bool=True, findRank:bool=False):
    # start from root, search for value
    nnode = self.root
    pathToRight = []
    while nnode != self.NULL:
      if value == nnode.value:
        if printResult:
          print('Find! The node looks like:')
          print(nnode)
          return
        elif findRank:
          rank = 0
          for node in pathToRight:
            rank += node.leftSize + 1
          return rank + nnode.leftSize + 1
        else:
          print('Find!')
          return nnode
      elif value > nnode.value:   
        if findRank:
          pathToRight.append(nnode)
        nnode = nnode.right
      else:
        nnode = nnode.left

    raise ValueError('Oops! can\'t find the Node.')

  def __searchNode(self, value):
    # start from root, search for node
    pnode = None
    nnode = self.root
    pathToLeft = []
    
    while nnode != self.NULL:
      pnode = nnode
      if value == nnode.value:
        raise ValueError('Key value is already in tree!')
      elif value < nnode.value:
        pathToLeft.append(nnode)
        nnode = nnode.left
      else:
        nnode = nnode.right
    
    return nnode, pnode, pathToLeft
          
  # left rotation at node
  def __leftRotate(self, node):
    rnode = node.right
    node.right = rnode.left

    if rnode.left != self.NULL:
      rnode.left.parent = node

    rnode.parent = node.parent
    if node.parent == None:
      self.root = rnode
    elif node == node.parent.left:
      node.parent.left = rnode
    else:
      node.parent.right = rnode
    rnode.left = node
    node.parent = rnode

    rnode.leftSize = rnode.leftSize + node.leftSize + 1

  # right rotation at node
  def __rightRotate(self, node):
    lnode = node.left
    node.left = lnode.right

    if lnode.right != self.NULL:
      lnode.right.parent = node

    lnode.parent = node.parent
    if node.parent == None:
      self.root = lnode
    elif node == node.parent.right:
      node.parent.right = lnode
    else:
      node.parent.left = lnode
    lnode.right = node
    node.parent = lnode

    node.leftSize = node.leftSize - (lnode.leftSize + 1)

  def insert(self, value:int, data=None, modify=True, color = 1) -> None:
    if not isinstance(value, int):
        raise TypeError('value must be integer!')
    if color not in [0,1]:
        raise ValueError('color must be 0 or 1!')

    nnode, pnode, pathToLeft = self.__searchNode(value)

    tnode = self.Node(value, color=color)
    tnode.left = self.NULL
    tnode.right = self.NULL
    tnode.data = data

    for n in pathToLeft:
      n.leftSize +=1

    # assign parent
    tnode.parent = pnode

    if pnode == None:
      # root
      self.root = tnode
      tnode.color = 0
      self.black+=1

    elif tnode.value < pnode.value:
      # insert left
      pnode.left = tnode
      self.red +=1
    
    else:
      # insert right
      pnode.right = tnode
      self.red +=1

    # keep the length
    self.length += 1
    # modify the tree
    self.__modify(tnode,modify)

  # modify the RBT
  def __modify(self, node, modify):
    def __makechanges(self, pnode, gpnode):
      # case 2, uncle is NULL, or uncle is not NULL but black.
      if gpnode.right == pnode:        
        if pnode.left == node:
          # case 2-1, gpnode's right is pnode, pnode's left is node.
          self.__rightRotate(pnode)
          self.__leftRotate(gpnode)
          node.color = 0
          gpnode.color = 1
        else:
          # case 2-2, gpnode's right is pnode, pnode's right is node.
          self.__leftRotate(gpnode)
          # recolor
          pnode.color = 0
          gpnode.color = 1
      else:
        if pnode.left == node:
          # case 2-3, gpnode's left is pnode, pnode's left is node.
          self.__rightRotate(gpnode)
          # recolor
          pnode.color = 0
          gpnode.color = 1
        else:
          # case 2-4, gpnode's left is pnode, pnode's right is node.
          self.__leftRotate(pnode)
          self.__rightRotate(gpnode)
          node.color = 0
          gpnode.color = 1

    Flag=True

    while node.color == 1 and Flag and modify:
      pnode = node.parent
      gpnode = pnode.parent if pnode != None else None

      # base case
      if node == self.root:
        # do nothing and return
        return
      elif pnode.color == 1:
        unode = gpnode.left if pnode == gpnode.right else gpnode.right
        if unode != self.NULL:
          if unode.color == 1:
            # case 1, uncle is red and not NULL: just simply recolor parent, uncle, and grandparent.
            if gpnode != self.root:
              gpnode.color = 1
              self.red += 1
              self.black -= 1
            unode.color = 0
            pnode.color = 0
            self.red -= 2
            self.black += 2
          # Propogate next iter to grandparent node.
            node = gpnode
            continue
          else:
            # case 2-1, uncle is black and not NULL.
            __makechanges(self, pnode, gpnode)
            
        else:
          # case 2-2, uncle is NULL. 
          __makechanges(self, pnode, gpnode)

      Flag=False    

  @typeCheck
  def delete(self, value: Union[int, list]) -> None:
    # if not (isinstance(value, int) or isinstance(value, list)):
    #     raise TypeError('value must be integer or list!')

    if isinstance(value, int):

      node = self.search(value, printResult=False)

      if node == self.NULL:
        print(f'Oops! the node {value} is not in the tree.')
        return 
      else:
        self.length -= 1
        self.__delete(node)

    elif isinstance(value, list):
      if len(value) == 0:
        print("You enter an empty list.")
        return 
      for v in value:
        node = self.search(v, printResult=False)
        if node == self.NULL:
          print(f'Oops! the node {v} is not in the tree.')
          continue
        else:
          self.length -= 1
          self.__delete(node)

  def __delete(self, node):
    # if node has two childrens, convert to 0 or 1 child node.
    if node.left != self.NULL and node.right != self.NULL:
      sucnode = self.successor(node.value)
      node.value = sucnode.value

      self.__delete(sucnode)

    elif node == self.root and node.left == self.NULL and node.right == self.NULL:
      self.root = self.NULL
      self.root.parent = None
      self.black -= 1
    else:     
      if node.color == 1:
        # if the node is red.
        if node.parent.left == node:
          node.parent.left = node.right
        else:
          node.parent.right = node.left
        self.red -= 1
      elif node.color == 0 and (node.right.color + node.left.color == 1):
        # if the node is black and has only one red child.
        if node.right != self.NULL:
          if node == self.root:
            self.root = node.right
            self.root.color = 0
            self.parent = None
          else:
            if node.parent.left == node:
              node.parent.left = node.right
            else:
              node.parent.right = node.right
            node.right.parent = node.parent
            node.right.color = 0
          self.red -= 1
          # self.black += 1
        else:
          if node == self.root:
            self.root = node.left
            self.root.color = 0
            self.parent = None
          else:
            if node.parent.left == node:
              node.parent.left = node.left
            else:
              node.parent.right = node.left
            node.left.parent = node.parent
            node.left.color = 0
          self.red -= 1
          # self.black+=1
      else:
        flag = 0
        inner_flag = 1
     
        # enter 6 cases
        self.__deleteModify(node, flag, inner_flag)

  def __deleteModify(self, node, flag, inner_flag):
    def __case5(node, pnode, snode):
      if pnode.left == node:
        return snode.color == 0 and snode.left.color == 1 and snode.right.color == 0
      else:
        return snode.color == 0 and snode.right.color == 1 and snode.left.color == 0
    # if the node is black.
    if node == self.root:
      # case 1, terminated case.
      flag = 1
    else:
      pnode = node.parent
      snode = pnode.left if (pnode.left != node and pnode.left != self.NULL) else pnode.right

      if pnode.color == 0 and snode.color == 1 and (snode.left.color + snode.right.color == 0):
        # case 2
        if node.parent.left == node:       
          self.__leftRotate(pnode)
        else:   
          self.__rightRotate(pnode)
        
          
        pnode.color = 1
        snode.color = 0

        self.__deleteModify(node, flag, inner_flag=0)

        if inner_flag:
          if node.parent.left == node:       
            node.parent.left = node.right
          else:
            node.parent.right = node.left

          if node.color == 1:
            self.red-=1
          else:
            self.black-=1

      elif pnode.color == 0 and snode.color == 0 and (snode.left.color + snode.right.color == 0):
        # case 3
        if inner_flag:
          if node.parent.left == node:
            node.parent.left = node.right
          else:
            node.parent.right = node.left

          if node.color == 1:
            self.red-=1
          else:
            self.black-=1
          
        snode.color = 1

        self.__deleteModify(pnode, flag, inner_flag=0)
        self.black-=1
        self.red+=1

      elif pnode.color == 1 and snode.color == 0 and (snode.left.color + snode.right.color) == 0:
        flag = 1
        # case 4, terminated case.

        pnode.color = 0
        snode.color = 1

      elif __case5(node, pnode, snode):
        # case 5
        if node.parent.left == node:
          self.__rightRotate(snode)
        else:
          self.__leftRotate(snode)
        snode.color = 1
        snode.parent.color = 0

        self.__deleteModify(node, flag, inner_flag)

      elif snode.color == 0 and (snode.left.color == 1 or snode.right.color == 1):
        # case 6, terminated case.
        flag = 1
        # if pnode.left == node:
        if pnode.left.value == node.value:
          self.__leftRotate(pnode)
          snode.color = pnode.color
          pnode.color = 0
          snode.right.color = 0
        else:
          self.__rightRotate(pnode)
          snode.color = pnode.color
          pnode.color = 0
          snode.left.color = 0
        self.red-=1
        self.black+=1

    if flag and inner_flag:
      if node.parent.left == node:
        if node.left == self.NULL:
          node.parent.left = node.right
        else:
          node.parent.left = node.left
      else:
        if node.left == self.NULL:
          node.parent.right = node.right
        else:
          node.parent.right = node.left
      if node.color == 1:
        self.red-=1
      else:
        self.black-=1
      return

  # return minNode
  def minNode(self, node=None):
    if node == None:
      node = self.root
    while node.left != self.NULL:
      node = node.left
    return node

  # return maxNode
  def maxNode(self, node=None):
    if node == None:
      node = self.root
    while node.right != self.NULL:
        node = node.right
    return node

  @typeCheck
  def successor(self, value: int):
    node = self.search(value, printResult=False)

    if node == None or node is self.NULL:
      return None
    if node.right != self.NULL:
      return self.minNode(node.right)

    pnode = node.parent
    while pnode != None and node == pnode.right:
      node = pnode
      pnode = node.parent
    return pnode

  @typeCheck
  def predecessor(self, value: int):
      node = self.search(value, printResult=False)

      if node == None or node is self.NULL:
        return None
      if node.left != self.NULL:
        return self.maxNode(node.left)

      pnode = node.parent
      while pnode != None and node == pnode.left:
        node = pnode
        pnode = node.parent
      return pnode

  def print(self):
    stack = [self.root]
    see = set()

    while stack:
      node = stack.pop()
      if node.left != self.NULL and node.left.value not in see:
        stack.append(node)
        stack.append(node.left)
      else:
        see.add(node.value)
        if node.right != self.NULL:
          stack.append(node.right)
    return see

  def rank(self, order:int):
    output = order
    if order > self.length:
      return 'The rank is bigger than tree length.'
    elif order <= 0:
      return 'The rank must be greater than 0.'
    stack = [self.root]
    while stack:
      nnode = stack.pop()
      if order < nnode.leftSize + 1:
        stack.append(nnode.left)
      elif order > nnode.leftSize + 1:
        order -= nnode.leftSize + 1 
        stack.append(nnode.right)
    return f'The rank {output} of node is {nnode.value}.'

  def select(self, value:int) -> int:
    order = self.search(value, printResult = False, findRank = True)
    return f'The selected node {value}\'s rank is {order}.'
