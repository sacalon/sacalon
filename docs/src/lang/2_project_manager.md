# Builtin Project Manager
Hascal has a builtin build system and project manager. This tool builds and runs your project, installs dependencies.

## Creating a new project
Let's create a new project and compare it with the Hello World example in previous chapter.

To create a project you should create a directory for your project :
```
$ mkdir hello_world_2
$ cd hello_world_2
```

Now we create a new project with following command :
```
$ hascal init
```

After running above command, you’ll see Hascal has generated two files and one directory for us: a `config.json` file, a `.gitignore` file and a `src` directory with a `app.has` file inside.

`config.json` :
```json
{
	"filename": "src/app.has", 
	"outfile": "build/app", 
}
```

The `filename` field contains your main file that contains your entry function(`main`) and `outfile` field is output path of excutable file.

`src/app.has` :
```typescript
function main():int{
	print("Hello World!")
	return 0
}
```

The generated Hascal file contains *Hello World!* program, you can edit it.

## Building a project
You can build the project with following command :
```
$ hascal build
```

Excutable file will generate in `build` directory and you can run it with following command :
```
$ ./build/app
```

## Running a project
To run the project, you can use `run` command :
```
$ hascal run
Hello World!
```

That builds excutable file and runs it.