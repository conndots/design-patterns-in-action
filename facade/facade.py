#!/usr/bin/python
# -*- coding : utf-8 -*-
"""
Facade pattern:
Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.
"""

#subsystem class
class PreProcessor:
	def process(self, input):
		print("Preprocessing code: {}".format(input))
		return input.replace(' ', '_')

#subsystem class
class Compiler:
	def process(self, input):
		print("Compiling code: {}".format(input))
		return input.upper()

#subsystem class
class Assembly:
	def process(self, input):
		print("Assembly: {}".format(input))
		return input.lower()

#subsystem class
class Linker:
	def process(self, input):
		print("Linking: {}".format(input))
		return '_'.join(input)

#facade
class CCompiler:
	def get_executable(self, src):
		last = src
		for processor in [PreProcessor(), Compiler(), Assembly(), Linker()]:
			last = processor.process(last)
		return last

def main():
	cc = CCompiler()
	print("EXE: {}".format(cc.get_executable("int main(){ printf(\"Hello world\"); }")))

if __name__ == '__main__':
	main()

"""
OUTPUT:
Preprocessing code: int main(){ printf("Hello world"); }
Compiling code: int_main(){_printf("Hello_world");_}
Assembly: INT_MAIN(){_PRINTF("HELLO_WORLD");_}
Linking: int_main(){_printf("hello_world");_}
EXE: i_n_t___m_a_i_n_(_)_{___p_r_i_n_t_f_(_"_h_e_l_l_o___w_o_r_l_d_"_)_;___}
"""
