"""
Proxy pattern:
Provide a surrogate or placeholder for another object to control access to it.

Here we use Proxy pattern to impelement copy-on-write strategy. It is related to creation on demand. 
Only the file has the copy-on-write feature. The directory with copy-on-write is a little complicated and weird.
"""
import functools

NODE_ID = -1
def get_nodeID():
	global NODE_ID
	NODE_ID += 1
	return NODE_ID

def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			print('{}: execute {}'.format(text, func.__name__))
			return func(*args, **kw)
		return wrapper
	return decorator

class FSElem:
	def __init__(self, name, par):
		self._name = name
		self._par = par
		self._id = get_nodeID()

	@property
	def id(self):
	    return self._id

	def __str__(self):
		return self._name

class Dir(FSElem):
	@log('init a directory')
	def __init__(self, name, par):
		super(Dir, self).__init__(name + '/', par)
		self._list = []

	def cp(self, par):
		dir = Dir(self._name, par)
		for e in self._list:
			dir._list.append(e.cp(e._name, dir))
		return dir

	def ls(self):
		return [elem.__str__() for elem in self._list]

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

	

class File(FSElem):
	@log('init a file')
	def __init__(self, name, content, par):
		super(File, self).__init__(name, par)
		self._content = content

	@property
	def id(self):
	    return self._id
	

	def cp(self, par):
		copy = File(self._name, self._content, par)
		return copy

	def __str__(self):
		return self._name + '(' + self._content + ')'

	@property
	def content(self):
	    return self._content
	
	@content.setter
	def content(self, content):
		self._content = content	 

#base proxy class: copy-on-write proxy
class COWProxy:
	def __init__(self, ref, par):
		self._ref = ref
		self._refed = []
		self._par = par

	@property
	def id(self):
		ref = self._ref
		while not isinstance(ref, FSElem):
			ref = ref._ref
		return ref.id
	
	@log('Actually do copy it')
	def _do_copy(self):
		if isinstance(self._ref, FSElem):
			return
		ref = self._ref
		while not isinstance(ref, FSElem):
			ref = ref._ref
		cp = ref.cp(self._par)
		self._ref = cp

	@log('COW')
	def _copy_on_write(self):
		if isinstance(self._ref, FSElem):
			return 
		for cp in self._refed:
			cp._do_copy()
		self._refed.clear()

		self._ref._refed.remove(self)
		self._do_copy()

	def __str__(self):
		return self._ref.__str__()

#proxy class for Dir
class DirProxy(COWProxy):
	@log('Init a directory proxy')
	def __init__(self, anything, par):
		if isinstance(anything, DirProxy) or isinstance(anything, Dir):
			super(DirProxy, self).__init__(anything, par)
		else:
			super(DirProxy, self).__init__(Dir(anything, par), par)

	#not copying the dir when call cp
	"""
	@log('just copy')
	def cp(self, par):
		if not isinstance(par, DirProxy):
			raise ValueError("dir must be a DirProxy instance.")
		cp = DirProxy(self, par)
		self._refed.append(cp)

		if isinstance(par._ref, Dir):
			par._ref._list.append(cp)
		else:
			par._copy_on_write()
			par._ref._list.append(cp)

		return cp
	"""
	@log('do copy')
	def cp(self, par):
		cp = self._ref.cp(par)
		par._ref._list.append(cp)
		return cp

	@log('list dirs and files')
	def ls(self):
		return self._ref.ls()

	@log('change directory')
	def cd(self, target):
		return self._ref.cd(target)
	

	@log('make a directory')
	def mkdir(self, name):
		if isinstance(self._ref, Dir):
			return DirProxy(self._ref.mkdir(name), self)
		#self._copy_on_write()
		#return DirProxy(self._ref.mkdir(name), self)

	@log('create a file')
	def create_file(self, name, content):
		if isinstance(self._ref, Dir):
			return FileProxy(self._ref.create_file(name, content), self)
		#self._copy_on_write()
		#return FileProxy(self._ref.create_file(name, content), self)

class FileProxy(COWProxy):
	@log('init a file proxy')
	def __init__(self, name, content, par):
		super(FileProxy, self).__init__(File(name, content, par), par)

	@log('init a file proxy')
	def __init__(self, ref, par):
		if isinstance(ref, File) or isinstance(ref, FileProxy):
			super(FileProxy, self).__init__(ref, par)
		else:
			raise ValueError("The ref must be a File or FileAgent")

	@property
	def name(self):
	    return self._ref._name

	@property
	def content(self):
	    return self._ref._content
	
	
	@log('just copy')
	def cp(self, par):
		if not isinstance(par, DirProxy):
			raise ValueError("dir must be a DirProxy instance.")
		cp = FileProxy(self, par)
		self._refed.append(cp)

		return cp

	@property
	def content(self):
	    return self._ref.content

	@content.setter
	@log('change file content')	
	def content(self, content):
		if isinstance(self._ref, File):
			self._ref.content = content
		else:
			self._copy_on_write()
			self._ref.content = content

	def __str__(self):
		return self._ref.__str__()

def main():
	root = DirProxy('root', None)
	dir_1 = root.mkdir('1')
	dir_2 = root.mkdir('2')
	dir_11 = dir_1.mkdir('1_1')
	readme = dir_11.create_file('README.md', "I am oringinal.")
	readme_cp = readme.cp(dir_2)
	readme_cp1 = readme_cp.cp(dir_1)

	print("!!! readme:[{}];readme copy: [{}];readme copy copy: [{}]".format(readme.__str__(), readme_cp.__str__(), readme_cp1.__str__()))

	readme_cp.content = "I am a copy. I am different."
	print("!!! readme:[{}];readme copy: [{}];readme copy copy: [{}]".format(readme.__str__(), readme_cp.__str__(), readme_cp1.__str__()))


if __name__ == '__main__':
	main()


"""
OUTPUT:
Init a directory proxy: execute __init__
init a directory: execute __init__
make a directory: execute mkdir
init a directory: execute __init__
Init a directory proxy: execute __init__
make a directory: execute mkdir
init a directory: execute __init__
Init a directory proxy: execute __init__
make a directory: execute mkdir
init a directory: execute __init__
Init a directory proxy: execute __init__
create a file: execute create_file
init a file: execute __init__
init a file proxy: execute __init__
just copy: execute cp
init a file proxy: execute __init__
just copy: execute cp
init a file proxy: execute __init__
!!! readme:[README.md(I am oringinal.)];readme copy: [README.md(I am oringinal.)];readme copy copy: [README.md(I am oringinal.)]
change file content: execute content
COW: execute _copy_on_write
Actually do copy it: execute _do_copy
init a file: execute __init__
Actually do copy it: execute _do_copy
init a file: execute __init__
!!! readme:[README.md(I am oringinal.)];readme copy: [README.md(I am a copy. I am different.)];readme copy copy: [README.md(I am oringinal.)]
"""










