# Typescript

* Allows definition of string types
* Need a typescript compiler for compiling ts to js
* `npm install typescript` The typescript package includes the typescript compiler `tsc`
* `tsconfig.json` configures the typescript options for the project e.g. ts compile options
* Needs a definition of the types provided in external libraries e.g. Angular

## TypeScript Definition file

* Describes the types defined in external libraries
* `.d.ts` file (not deployed, just used for compilation, editors use these for auto completion)
* Need a ts definition file per external library or framework we use and they can be found here: https://definitelytyped.org/
* `npm install tsd` Package manager for ts definition files
* `tsd install angular --resolve --save` Installs angular ts type definitions and resolves its dependencies (e.g angular depends on jquery) and save this action to a `tsd.json` file in the project. This will create
    * `angular.d.ts`
    * `jquery.d.ts` files in a `typings` directory.

## Typescript modules

* Encapsulate variables, interfaces and classes
* Define unique namespaces like other languages (C#, Java)
    * `System.IO`
    * `java.io`