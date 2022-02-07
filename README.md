# Quick project setup script for Next.Js projects
The main goal of this script is to speed up initial setup for simple Next.Js projects. I hope it will be useful for you as well. Feel free to modify and use it.

## Requirements:
- Node.js
- Next.js
- Python
- VS Code installed

## Usage:
  Copy this file to the directory where you want to create the project folder of the
  new Next.Js app.
  To run the script use cmd:<br />
  `python main.py`<br />
  The script will ask for a project name. This will also be the name of the freshly created folder.
  Then Create-next-app is called. After completion, the script enters the newly created
  project folder and installs the specified dependencies, updates the package.json and next.config.js files,
  creates a folder structure for SASS, deletes some unnecessary files and updates index.js. After all done, VS Code is launched.
  The result will be a minimal Next.Js app setup with simple build process set up for 7-1 SASS architecture with NPM scripts and Next export for SSG.<br />
  <br />
  Additionally you should modify at least the following in package.json:<br />
  "concat:css": "concat -o styles/globals.concat.css **styles/linea.css** styles/globals.comp.css"<br />
  Provide your 3rd party css files instead of the bold one so they will be concatenated to the compiled css. This will result in a single minified css in the end.<br /><br />
  
  `npm run nextdevandsass` run dev and watch sass<br />
  `npm run build:css` builds minified css<br />
  `npm run export` builds next.js app and creates out folder for SSG<br />
<br />
## The following npm packages are used:
  ### As dev dependency:
     - node-sass
     - concat
     - autoprefixer
     - postcss-cli
     - npm-run-all
  ### As dependency:
     - next-images
     - next-videos
<br /><br />
### Future plans:
    - Add initial content in sass files following BEM methodology (Initial CSS reset, etc.)
    - Create reusable component directory
    - Automatically add reusable components that are required based on the app prototype
    - Convert all images to webp, create multiple versions for density and resolution switching
