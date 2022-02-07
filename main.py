# ---------------------------------------------------------------------------------------------
# Quick project setup script for Next.Js projects.
#
#
# (c) 2022 Zoltán Séra, Tés, Hungary
# Released under the MIT License
# email dev.zoltan.sera@gmail.com
#
# Usage:
#   Copy this file to the directory where you want to create the project folder of the
#   new Next Js app. After running the script, it will ask for a project name. This will also
#   be the name of the freshly created folder.
#   Then Create-next-app is called. After completion, the script enters the newly created
#   project folder and installs the specified dependencies, updates the package.json and next.config.js files,
#   creates a folder structure for SASS, deletes some unnecessary files and updates index.js.
#   The result will be a minimal Next.Js app setup.
#
# Adds the following:
#   As dev dependency:
#       - node-sass
#       - concat
#       - autoprefixer
#       - postcss-cli
#       - npm-run-all
#   As dependency:
#       - next-images
#       - next-videos
#
# ---------------------------------------------------------------------------------------------
#
# The MIT License (MIT)
#
# Copyright (c) 2022, Zoltán Séra
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# ---------------------------------------------------------------------------------------------


import os

dev_dependencies = [
    "node-sass",
    "concat",
    "autoprefixer",
    "postcss-cli",
    "npm-run-all"
]

prod_dependencies = [
    "next-images",
    "next-videos"
]

sass_directory_structure = {
    "abstracts": ["_functions.scss", "_mixins.scss", "_variables.scss"],
    "base": ["_animations.scss", "_base.scss", "_typography.scss", "_utilities.scss"],
    "components": [],
    "layout": [],
    "pages": ["_home.scss"],
    "themes": [],
    "vendors": []
}

# Ask user for project name
app_name = input("Create Next app with the following name: ")
print("--- NEXT.JS PROJECT SETUP STARTED ---")

create_next_app_cmd = f"start /WAIT cmd /c npx create-next-app {app_name}"
install_npm_packages_cmd = (
        f"cd {app_name} && npm install " + " ".join(dev_dependencies) + " --save-dev && "
        f"npm install " + " ".join(prod_dependencies)
        )

# CALL CREATE-NEXT-APP with the provided app name
if app_name.isalnum():
    print("------ Creating Next.Js app")
    os.system(create_next_app_cmd)
    print("------ Installing NPM packages")
    os.system(install_npm_packages_cmd)

# Modify package.json
print("------ Setting up package.json")
package_json_path = f"{app_name}/package.json"
new_package_json_content = ""
with open(package_json_path) as file_obj:
    for line in file_obj:
        new_package_json_content += line
        if '"scripts": {' in line:
            new_package_json_content += (
                '\t\t"nextdevandsass": "npm-run-all --parallel dev watch:sass",\n'
                '\t\t"watch:sass": "node-sass sass/main.scss styles/globals.css -w",\n'
                '\t\t"compile:sass": "node-sass sass/main.scss styles/globals.comp.css",\n'
                '\t\t"concat:css": "concat -o styles/globals.concat.css styles/linea.css styles/globals.comp.css",\n'
                '\t\t"prefix:css": "postcss --use autoprefixer -b \'last 10 versions\' styles/globals.concat.css -o'
                ' styles/globals.prefix.css",\n'
                '\t\t"compress:css": "node-sass styles/globals.prefix.css styles/globals.min.css '
                '--output-style compressed",\n'
                '\t\t"build:css": "npm-run-all compile:sass concat:css prefix:css compress:css",\n'
                '\t\t"export": "next build && next export",\n'
            )

with open(package_json_path, "w") as file_obj:
    file_obj.write(new_package_json_content)

# Modify next.config.js
print("------ Setting up next.config.js")
next_config_path = f"{app_name}/next.config.js"
with open(next_config_path, "w") as file_obj:
    file_obj.write(
        'const withImages = require("next-images");\n'
        'const withVideos = require("next-videos");\n\n'
        'module.exports = withImages(withVideos({\n'
        '\treactStrictMode: true,\n'
        '\timages: {\n'
        '\t\tdisableStaticImages: true,\n'
        '\t\tloader: "imgix",\n'
        '\t\tpath: "",\n\t}\n}));'
    )

# Creating SASS folder structure
print("------ Creating SASS folder structure (7-1 architecture)")
new_dir = f"{app_name}/sass"
main_scss_file = f"{new_dir}/main.scss"


def add_main_scss_import(dir_name, file_name):
    with open(main_scss_file, "a") as main_scss:
        import_name = f'@import "{dir_name}/{file_name[1:].replace(".scss", "")}";\n'
        main_scss.write(import_name)


def create_empty_scss_file(dir_name, file_name):
    if len(file_name) > 6:
        new_file_name = f"{dir_name}/{file_name}"
        with open(new_file_name, "w") as nf:
            nf.write("")
        add_main_scss_import(dir_name.replace(f"{app_name}/sass/", ""), file_name)


os.mkdir(new_dir)
with open(main_scss_file, "w") as fo:
    fo.write("")

for subdir in sass_directory_structure:
    new_sub_dir = f"{new_dir}/{subdir}"
    os.mkdir(new_sub_dir)
    for item in sass_directory_structure[subdir]:
        create_empty_scss_file(new_sub_dir, item)

# Creating bare minimum index.js
print("------ Creating bare minimum index.js")
index_js_file = f"{app_name}/pages/index.js"
index_js_content = (
                    "import Head from 'next/head'\n\n"
                    "export default function Home() {\n"
                    "\treturn (\n"
                    "\t\t<>\n"
                    "\t\t\t<Head>\n"
                    "\t\t\t\t<meta charSet=\"UTF-8\" />\n"
                    "\t\t\t\t<title>Create Next App</title>\n"
                    "\t\t\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
                    "\t\t\t\t<meta httpEquiv=\"X-UA-Compatible\" content=\"ie=edge\" />\n\n"
                    "\t\t\t\t<meta name=\"description\" content=\"Generated by create next app\" />\n\n"
                    "\t\t\t\t<meta property=\"og:title\" content=\"OG:TITLE\" />\n"
                    "\t\t\t\t<meta property=\"og:site_name\" content=\"OG:SITENAME\" />\n"
                    "\t\t\t\t<meta property=\"og:url\" content=\"OG:URL\" />\n"
                    "\t\t\t\t<meta property=\"og:description\" content=\"OG:DESC \" />\n"
                    "\t\t\t\t<meta property=\"og:type\" content=\"website\" />\n"
                    "\t\t\t\t<meta property=\"og:image\" content=\"https://mysite.hu/img/my_img.webp\" />\n\n"
                    "\t\t\t\t<link rel=\"icon\" href=\"/favicon.ico\" />\n"
                    "\t\t\t</Head>\n"
                    "\t\t\t<header>\n\t\t\t</header>\n"
                    "\t\t\t<main>\n\t\t\t\t<section>\n\t\t\t\t</section>\n\t\t\t</main>\n"
                    "\t\t\t<footer>\n\t\t\t</footer>\n"
                    "\t\t</>\n"
                    "\t)\n"
                    "}"
                    )

with open(index_js_file, "w") as index_js:
    index_js.write(index_js_content)

# Removing unnecessary components
# CSS modules won't be used, minified css will be created of the compiled sass code using:  build:css (line 60)
print("------ Removing unnecessary components")
files_to_delete = [
    f"{app_name}/styles/Home.module.css",
    f"{app_name}/public/vercel.svg"
]
for file in files_to_delete:
    os.remove(file)


print("--- NEXT.JS PROJECT SETUP DONE ---")
print("--- Opening project in VS Code")
open_project_in_vs_code_cmd = f"cd {app_name} && code ."
os.system(open_project_in_vs_code_cmd)
