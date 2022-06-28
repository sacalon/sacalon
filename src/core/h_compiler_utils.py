
class Var(object):
    """
    Variable object to store variable information

    Attributes:
        name (str): Name of the variable
        type (str): Type of the variable
        is_array (bool): Whether the variable is an array
        members (dict): Dictionary of members of the variable
        nullable (bool): Whether the variable is nullable
    """

    def __init__(self, name, type, is_array=False, members={}, nullable=False):
        self.name = name
        self.type = type
        self.is_array = is_array
        self.members = members
        self.nullable = nullable


class Const(Var):
    ...


class Function(object):
    """
    Function object to store function information

    Args:
        name (str): Name of the function
        params (dict): Dictionary of parameters of the function
        return_type (str): Return type of the function
    """
    def __init__(self, name, params, return_type):
        self.name = name
        self.params = params  # type : dict
        self.return_type = return_type


class Struct(object):
    """
    Struct object to store struct information

    Args:
        name (str): Name of the struct
        members (dict): Dictionary of members of the struct
        category (str): Category of the struct
        is_ptr (bool): Whether the struct is a pointer
        ptr_str (str): Pointer string of the struct
        nullable (bool): Whether the struct is nullable
    """

    def __init__(
        self, name, members, category="", is_ptr=False, ptr_str="", nullable=False
    ):
        self.name = name
        self.members = members
        self.stdtype = False
        self.is_ptr = is_ptr
        self.ptr_str = ptr_str
        self.category = name
        self.nullable = nullable

    def __str__(self):
        return self.get_type_name()

    def get_type_name(self):
        return self.name + self.ptr_str


class Enum(Struct):
    ...


class Type(object):
    """
    Type object to store type information

    Args:
        type_name (str): Name of the type
        stdtype (bool): Whether the type is a standard type
        category (str): Category of the type
        is_ptr (bool): Whether the type is a pointer
        ptr_str (str): Pointer string of the type
        nullable (bool): Whether the type is nullable
    """
    def __init__(
        self, type_name, stdtype, category="", is_ptr=False, ptr_str="", nullable=False
    ):
        self.type_name = type_name
        self.stdtype = stdtype
        self.is_ptr = is_ptr
        self.ptr_str = ptr_str
        self.category = category
        self.nullable = nullable

    def __str__(self):
        return self.get_type_name()

    def get_type_name(self):
        """
        Returns the type name of the type

        Returns:
            str: Type name of the type
        """

        if self.is_ptr:
            return "%s%s" % (self.type_name, self.ptr_str)
        else:
            return self.type_name + self.ptr_str

    def get_name_for_error(self):
        """
        Returns the name of the type for error messages

        Returns:
            str: Name of the type for error messages
        """

        ptr_str = self.ptr_str.replace("*", "^")

        if self.is_ptr:
            return "%s%s" % (self.type_name, ptr_str)
        else:
            return self.type_name + ptr_str


class Array(Type):
    """
    Array object to store array information

    Args:
        type_obj (Type): Type object of the array
        is_ptr (bool): Whether the array is a pointer
        ptr_str (str): Pointer string of the array
    """
    def __init__(self, type_obj, is_ptr=False, ptr_str=""):
        self.type_obj = type_obj
        self.is_ptr = is_ptr
        self.ptr_str = ptr_str
        if isinstance(type_obj, Type):
            super().__init__(type_obj.type_name, type_obj.stdtype)
        elif isinstance(type_obj, Struct):
            super().__init__(type_obj.name, type_obj.members)

    def __str__(self):
        if isinstance(self.type_obj, Type):
            return "std::vector<%s>%s" % (self.ptr_str, self.get_type_name())
        elif isinstance(self.type_obj, Struct):
            return "std::vector<%s>%s" % (str(self.type_obj), self.ptr_str)

    def get_name_for_error(self):
        """
        Returns the name of the array for error messages

        Returns:
            str: Name of the array for error messages
        """
        ptr_str = self.ptr_str.replace("*", "^")

        if isinstance(self.type_obj, Type):
            return "[%s]%s" % (self.ptr_str, self.get_type_name())
        elif isinstance(self.type_obj, Struct):
            return "[%s]%s" % (str(self.type_obj), self.ptr_str)

def return_null_according_to_type(type_, expr,name_,decl=True,array_decl=False):
    """
    Return null according to type

    Args:
        type_ (dict): type
        expr (dict): expression
        name_ (string): name
        decl (bool, optional): is declarator. Defaults to True.
        array_decl (bool, optional): is array declarator. Defaults to False.

    Returns:
        str: generated code
    """

    # Check if variable is literal or pointer and expr is null : set variable to `nullptr`
    if (
        expr["type"].category == "all-nullable"
        and str(type_["type"]) == "string"
    ):
        expr_ = "%s = nullptr;" % (name_)
    # Check if variable is vector and expr is null : set variable to `nullptr`
    elif (
        expr["type"].category == "all-nullable"
        and isinstance(type_["type"],Array)
    ):
        return "%s = nullptr;" % (name_)
    else :
        if decl :
            return "%s %s = %s;" % ("std::vector<"+str(type_["type"])+">" if array_decl else type_["type"], name_, expr["expr"]) 
        return "%s = %s;\n" % (name_, expr["expr"])
    return ""

def is_compatible_ptr(type_a, type_b):
    """
    Check if two pointer types are compatible

    Args:
        type_a (dict): type a
        type_b (dict): type b

    Returns:
        bool: True if compatible, False otherwise
    """
    if type_a.is_ptr == type_b.is_ptr:
        return True
    else:
        return False


def is_compatible_type(type_a, type_b):
    """
    Check if two types are compatible

    Args:
        type_a (dict): type a
        type_b (dict): type b
    
    Returns:
        bool: True if compatible, False otherwise
    """
    if type_a == type_b:
        return True
    if is_nullable_compatible_type(type_a, type_b):
        return True

    if isinstance(type_a, Type) and isinstance(type_b, Type):
        if str(type_a.category) == str(type_b.category) and is_compatible_ptr(
            type_a, type_b
        ):
            return True
        else:
            return False

    if isinstance(type_a, Struct) and isinstance(type_b, Struct):
        if str(type_a.category) == str(type_b.category) and is_compatible_ptr(
            type_a, type_b
        ):
            return True
        else:
            return False

    return False

def is_nullable(type_obj):
    """
    Check if the type is nullable

    Args:
        type_obj (dict): type object

    Returns:
        bool: True if nullable, False otherwise
    """

    if type_obj.nullable == True:
        return True
    return False


def is_nullable_compatible_type(type_a, type_b):
    """
    Check if two types are nullable compatible

    Args:
        type_a (dict): type a
        type_b (dict): type b

    Returns:
        bool: True if nullable compatible, False otherwise
    """
    
    if (is_nullable(type_a) == True and type_b.category == "all-nullable") or (
        is_nullable(type_b) == True and type_a.category == "all-nullable"
    ):
        return True
    if (is_nullable(type_a) == False and type_b.category == "all-nullable") or (
        is_nullable(type_b) == False and type_a.category == "all-nullable"
    ):
        return False

    return True
