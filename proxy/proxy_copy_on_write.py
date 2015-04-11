"""
Proxy pattern:
Provide a surrogate or placeholder for another object to control access to it.

Here we use Proxy pattern to impelement copy-on-write strategy. It is related to creation on demand. 
"""

class Dir:
	def __init__(self, name, par):
		if not isinstance(par, Dir):
			raise ValueError("Can only copy to a directory.")
		self._list = []
		self._name = name + '/'
		self._par = par

	def cp(self, par):
		if not isinstance(par, Dir):
			raise ValueError("Can only copy to a directory.")
		dir = Dir(self._name, par)
		par._list.append(dir)
		for e in self._list:
			dir._list.append(e.copy(e._name))
		return dir

	def ls(self):
		return [elem.__repr__() for elem in self._list]

	def cd(self, target):
		target_name = None	
		if target == '..':
			return self._par
		elif target.startswith('./'):
			target_name = target[2:]
		else:
			raise ValueError("Not supported changing directory action")
		return [elem for elem in self._list if elem._name == target_name][0]

	def mkdir(self, name):
		dir = Dir(name, self)
		self._list.append(dir)
		return dir

	def create_file(self, name, content):
		f = File(name, content, self)
		self._list.append(f)
		return f

	def __repr__(self):
		return self._name

class File:
	def __init__(self, name, content, par):
		self._name = name
		self._content = content
		self._par = par

	def cp(self, par):
		if not isinstance(par, Dir):
			raise ValueError("Can only copy to a directory.")

		copy = File(name, content, par)
		par._list.append(copy)

	def change_content(self, content):
		self._content = content

#base proxy class
class FSProxy:
	def __init__(self, ref, par):
		self._ref = ref
		self._refed = []
		self._par = par

	def _do_copy(self):
		cp = self._ref.cp(self._par)
		self._ref = cp

	def _copy_on_write(self):
		for cp in self._refed:
			cp._do_copy()
		self._refed.clear()

		self._ref._refed.remove(self)
		self._do_copy()

#proxy class for Dir
class DirProxy(FSProxy):
	def __init__(self, anything, par):
		if isinstance(anything, DirProxy):
			super(DirProxy, self).__init__(anything, par)
		else:
			super(DirProxy, self).__init__(Dir(anything, par), par)

	def __init__(self, ref, par):

	#not copying the dir when call cp
	def cp(self, par):
		if not isinstance(dir, DirProxy):
			raise ValueError("dir must be a DirProxy instance.")
		cp = DirProxy(self, par)
		self._refed.append(cp)
		return cp

	def ls(self):
		return self._ref.ls()

	def cd(self, target):
		return self._ref.cd(target)
	

	def mkdir(self, name):
		if isinstance(self._ref, Dir):
			return self._ref.mkdir(name)
		self._copy_on_write()
		return self._ref.mkdir(name)

	def create_file(self, name, content):
		if isinstance(self, Dir):
			return self._ref.create_file(name, content)
		self._copy_on_write()
		return self._ref.create_file(name, content)

class FileProxy(FSProxy):
	def __init__(self, name, content, par):
		super(FileProxy, self).__init__(File(name, content, par), par)

	def __init__(self, ref, par):
		super(FileProxy, self).__init__(File(name, content, par), par)

	def cp(self, par):
		if not isinstance(dir, DirProxy):
			raise ValueError("dir must be a DirProxy instance.")
		cp = FileProxy(self, par)
		self._refed.append(cp)
		return cp

	def change_content(self, content):
		if isinstance(self._ref, File):
			self._ref.change_content(content)
		else:
			self._copy_on_write()
			self._ref.change_content(content)












