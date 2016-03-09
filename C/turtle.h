#include <Python.h>
#include <stdio.h>

int _PY_STARTED = 0;
void *_PY_MAIN = NULL;
wchar_t *_PY_PROGRAM = NULL;


/**
 * Special types
 */
typedef struct {
    double x;
    double y;
} vec2D;


typedef struct {
    uint8_t R;
    uint8_t G;
    uint8_t B;
} Color;


/**
 * Ensure that the interpreter has been correctly initialized. Can be called multiple times, but all successive calls
 * are no-ops.
 */
void _start_interpreter(void) {
    if (_PY_STARTED == 0) {
        // Start python
        _PY_PROGRAM = Py_DecodeLocale("pytuga", NULL);
        Py_SetProgramName(_PY_PROGRAM);
        Py_Initialize();

        // Import important modules
        PyRun_SimpleString("import tugalib as _tubalib\n");
        _PY_MAIN = PyImport_AddModule("__main__");

        // Changed started flag
        _PY_STARTED = 1;
    }
}

void _finish_interpreter(void) {
    Py_Finalize();
    PyMem_RawFree(_PY_PROGRAM);
}


/**
 * Call a Python function in global namespace using formatted
 * variable specifier to set the type of each argument.
 *
 * This function just eval a string within python's
 * interpreter.
 */
void  _va_pycall(char* cmd, va_list argptr) {
    char formatted[2048];
    char buffer[2048];
    sprintf(buffer, "__result__ = %s", cmd);

    // Format command
    va_start(argptr, buffer);
    vfprintf(formatted, buffer, argptr);
    va_end(argptr);

    // Run in the interpreter
    _start_interpreter();
    PyRun_SimpleString(formatted);
}


void pycall(char* cmd, ...) {
    va_list argptr;
    _va_pycall(cmd, argptr);
}

int ipycall(char* cmd, ...) {
    va_list argptr;
    _va_pycall(cmd, argptr);

    // Get output
    PyObject *pyobj = PyObject_GetAttrString(_PY_MAIN, "__result__");
    int result = PyInt_AsLong(pyobj);
    Py_DecRef(pyobj);
    return result;
}

int fpycall(char* cmd, ...) {
    va_list argptr;
    _va_pycall(cmd, argptr);

    // Get output
    PyObject *pyobj = PyObject_GetAttrString(_PY_MAIN, "__result__");
    int result = PyFloat_AsDouble(pyobj);
    Py_DecRef(pyobj);
    return result;
}


/**
 * Turtle movement
 */
void lineto(double x, double y)  { pycall("_tugalib.lineto(%lf, %lf)", x, y); }
void forward(double px)          { pycall("_tugalib.forward(%lf)", px); }
void backward(double px)         { pycall("_tugalib.backward(%lf)", px); }
void left(double angle)          { pycall("_tugalib.left(%lf)", angle); }
void right(double angle)         { pycall("_tugalib.right(%lf)", angle); }
void penup(void)                 { pycall("_tugalib.penup()"); }
void pendown(void)               { pycall("_tugalib.pendown()"); }


/**
 * Set turtle state
 */
void setpos(double x, double y)    { pycall("_tugalib.setpos(%lf, %lf)", x, y); }
void setheading(double angle)      { pycall("_tugalib.setheading(%lf)", angle); }
void setwidth(double px)           { pycall("_tugalib.setwidth(%lf)", px); }
void setcolor(int R, int G, int B) { pycall("_tugalib.setcolor(%i, %i, %i)", R, G, B); }
void setfill(int R, int G, int B)  { pycall("_tugalib.setfill(%i, %i, %i)", R, G, B); }



/**
 * Get turtle state
 */
double getwidth(void)     { return fpycall("getwidth()"); }
double getheading(void)   { return fpycall("getheading()"); }

vec2D getpos(void) {
    vec2D pos;
    pycall("__vector__ = _tugalib.getpos()");
    pos.x = fpycall("__vector__.x");
    pos.y = fpycall("__vector__.y");
    return pos;
}


color getcolor(void) {
    Color color;

    pycall("__color__ = _tugalib.getcolor()");
    color.R = ipycall("__color__[0]");
    color.G = ipycall("__color__[1]");
    color.B = ipycall("__color__[2]");

    return color;
}

color getfill(void) {
    Color color;

    pycall("__color__ = _tugalib.getfill()");
    color.R = ipycall("__color__[0]");
    color.G = ipycall("__color__[1]");
    color.B = ipycall("__color__[2]");

    return color;
}