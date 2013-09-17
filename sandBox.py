import compiler

class sandBoxStaticModule:
    scriptName = ''
    scriptText = ''

    
    def __init__(self,scriptName, scriptText):
            self.scriptName = scriptName
            self.scriptText = scriptText
            
    def testStaticMain(self):
        print "Running Static tests..."
        self.checkScriptExtn()
        self.checkScriptNodes()
        print "Static tests completed successfully..."
 
    """
    A white list of nodes that will be checked in the script
    """   
    def generateWhiteListNodes(self):
        nodeWhiteList = [
            'Add', 'And', 'AssAttr', 'AssList', 'AssName', 'AssTuple', 'Assert', 'Assign', 'AugAssign',
            'Bitand', 'Bitor', 'Bitxor', 'Break',
            'CallFunc', 'Class', 'Compare', 'Const', 'Continue',
            'Decorators', 'Dict', 'Discard', 'Div',
            'Ellipsis', 'Expression', 'FloorDiv', 'For', 'Function',
            'Getattr', 'Global', 'If', 'IfExp', 'Invert', 'Keyword',
            'LeftShift', 'List', 'ListComp', 'ListCompFor', 'ListCompIf',
            'Mod', 'Module', 'Mul', 'Name', 'Not', 
            'Or', 'Pass', 'Power', 'Print', 'Printnl', 
            'Raise', 'Return', 'RightShift',
            'Slice', 'Sliceobj', 'Stmt', 'Sub', 'Subscript',
            'TryExcept', 'TryFinally', 'Tuple', 
            'UnaryAdd', 'UnarySub', 'While', 'Yield']
        return nodeWhiteList

    """
    The valid file extensions that sandbox can run 
    Python : .py
    """
    def generateWhiteListExtensions(self):
        extnWhiteList =['.py']
        return extnWhiteList
    
    """
    Raise error if the file extension not in white list of extensions in function : generateWhiteListExtensions()
    """    
    def checkScriptExtn(self):
        extnErr = 1
        validExtns = self.generateWhiteListExtensions()
        for eachExtn in validExtns:
            if self.scriptName.endswith(eachExtn):
                extnErr = 0
            else:
                extnErr = 1
        if extnErr == 1:
            raise Exception('Error: Not a supported extension')
        else:
            pass
    """
    Check for the abstract syntax tree(AST) generated through python compiler package check the right list of nodes in the AST
    """     
    def checkScriptNodes(self):
        scriptRootNode = compiler.parseFile(self.scriptName)
        self.traverseNodes(scriptRootNode)
        #print scriptRootNode
        
    """
    For the given nodes in check script check for the valid list of nodes in the generateWhiteNodes()
    """    
    def traverseNodes(self,nodeList):
        validNodes = self.generateWhiteListNodes()
        if nodeList.__class__.__name__ not in validNodes:
            raise Exception("Error: Invalid script code")  
        for childNode in nodeList.getChildNodes():
            self.traverseNodes(childNode)
            
            
            
class sandBoxDynamicModule:
    scriptName = ''
    scriptText = ''
    allFunctionsDict = {}
    allTypesDict = {}
    validExecDict = {}
    
    def __init__(self,scriptName, scriptText, validFunctionsDict, validTypesDict):
            self.scriptName = scriptName
            self.scriptText = scriptText
            self.allFunctionsDict = validFunctionsDict
            self.allTypesDict = validTypesDict
    
    def execSafeDict(self):
        self.validExecDict = dict(self.allFunctionsDict.items() + self.allTypesDict.items())    
    
    def testDynamicMain(self): 
        print "Running Dynamic tests..."
        self.execSafeDict()
        print "Executing Program in controlled environment..."  
        exec(self.scriptText, self.validExecDict)
        print "Dynamic tests completed successfully"


            
            
            
        