import sublime
import sublime_plugin
import re

class SmartBackspaceCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if len(self.view.sel()) == 1:
			region = self.view.sel()[0]
			if not(region.empty()):	# if there is a selection
				self.view.run_command('left_delete')
			else:
				caret = region.begin()
				full_line = self.view.full_line(caret)
				line_contents = self.view.substr(full_line)
				left_region = sublime.Region(full_line.begin(), caret)
				left_contents = self.view.substr(left_region)
				line_above = self.view.full_line(left_region.begin() - 1)
				above_contents = self.view.substr(line_above).strip()

				if len(line_contents.strip()) == 0: # if trimmed line empty
					if len(above_contents) == 0: # if the above line is empty
						# delete above line
						self.view.erase(edit, line_above)
					else:
						point_after_delete = left_region.begin() - 1
						# delete line
						self.view.run_command('run_macro_file', {"file": "res://Packages/Default/Delete Line.sublime-macro"})
						self.view.sel().clear();
						self.view.sel().add(sublime.Region(point_after_delete))
				elif len(left_contents) == 0: # if untrimmed region left is 0
					self.view.run_command('left_delete')
				elif len(left_contents.strip()) == 0: # if trimmed region left of cursor empty
					if full_line.begin() != 0: # if there is a line above
						if len(above_contents) == 0: # if the above line is empty
							# delete above line
							self.view.erase(edit, line_above)
						else:
							last_char_point = line_above.end() - 1
							while len(self.view.substr(last_char_point).strip()) == 0:
								last_char_point = last_char_point - 1
							last_char = self.view.substr(last_char_point)
							last_char_point = last_char_point + 1
							region_to_delete = sublime.Region(caret, last_char_point)
							self.view.erase(edit, region_to_delete)
							pattern = re.compile('\\w')
							if pattern.match(last_char):
								self.view.insert(edit, last_char_point, ' ')
					else:
						self.view.run_command('run_macro_file', {"file": "res://Packages/Default/Delete to Hard BOL.sublime-macro"})
				else:
					self.view.run_command('left_delete')
		else:
			self.view.run_command('left_delete')
