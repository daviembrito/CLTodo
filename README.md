# **CLTodo**
Command Line Todos list manager in Python

## **Installation**
```git clone https://github.com/daviembrito/CLTodo.git```

## **Usage**
```cd CLTodo```

```python CLTodo.py```

### **Commands**
<p>
    <table>
        <thead>
            <tr>
                <th>Command</th>
                <th>Parameters</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>lists</td>
                <td>None</td>
            </tr>
            <tr>
                <td>create</td>
                <td>Name</td>
            </tr>
            <tr>
                <td>delete</td>
                <td>Name</td>
            </tr>
            <tr>
                <td>select</td>
                <td>Name</td>
            </tr>
            <tr>
                <td>show</td>
                <td>None, [Category]</td>
            </tr>
            <tr>
                <td>add</td>
                <td>Todo, Category</td>
            </tr>
            <tr>
                <td>remove</td>
                <td>Position</td>
            </tr>
            <tr>
                <td>done</td>
                <td>Position</td>
            </tr>
            <tr>
                <td>change</td>
                <td>Position, NewPosition</td>
            </tr>
            <tr>
                <td>quit</td>
                <td>None</td>
            </tr>
            <tr>
                <td>help</td>
                <td>None</td>
            </tr>
        </tbody>
    </table>
</p>
<p></p>

### **lists**

List all Todos lists

### **create ```<```name```>```**

Creates a new list with name ```<```name```>```

### **delete ```<```list```>```**

Deletes a list with name ```<```list```>```

### **select ```<```name```>```**
Selects a list to interact with

### **show ```[```category```]```**
Shows the whole selected list or just a category

### **add ```<```todo```>``` ```<```category```>```**
Adds a new Todo with the specified informations

### **remove ```<```position```>```**
Removes a Todo with the specified position

### **done ```<```position```>```**
Changes the status of the Todo to "done" or "undone"

### **change ```<```pos```>``` ```<```new_pos```>```**
Changes a Todo's position

### **quit**
Quit the program

### **help**
Displays a help message

<p></p>

## **Examples**
<p></p>

![Creating list and todo](https://cdn.discordapp.com/attachments/400108474748370946/1090440511455768708/image.png)

<p></p>

![Removing todo](https://cdn.discordapp.com/attachments/400108474748370946/1090440769602584607/image.png)

<p></p>

![Show with category](https://cdn.discordapp.com/attachments/400108474748370946/1090443090029985832/image.png)