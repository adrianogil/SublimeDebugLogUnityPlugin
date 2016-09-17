import sublime, sublime_plugin

import re

class DebuglogCommand(sublime_plugin.TextCommand):
	clean_name = re.compile('^\s*(public\s+|private\s+|protected\s+|static\s+|function\s+|def\s+)+', re.I)
	def run(self, edit):
		# self.view.insert(edit, 0, "Hello, World!")
		view = self.view		

		index = 0

		for region in view.sel():
			s = ""
			region_row, region_col = view.rowcol(region.begin())
			found = False

			# Look for any classes
			# class_regions = view.find_by_selector('entity.name.type.class')
			class_regions = view.find_by_selector('entity.name.type')
			print(class_regions)
			for r in reversed(class_regions):
				row, col = view.rowcol(r.begin())
				if row <= region_row:
					s += view.substr(r)
					found = True
					break;

            # Look for any functions
			function_regions = view.find_by_selector('entity.name.function')
			print(function_regions)
			if function_regions:
				for r in reversed(function_regions):
					row, col = view.rowcol(r.begin())
					if row <= region_row:
						if s:
							s += "::"
						lines = view.substr(r).splitlines()
						name = self.clean_name.sub('', lines[0])
						s += name.strip()
						found = True
						break

			s = "Debug.Log(\"" + s + "\");" 

			print(str(index) + ": " + s)
			index = index + 1

			view.replace(edit, region, s)
			
