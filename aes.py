# -*- coding: utf-8 -*-
import sys
from colorama import init, Fore, Style
import random, string

class AES:
	def __init__(self):
		self.rcon0        = ['01', '00', '00', '00']
		self.rcon1        = ['02', '00', '00', '00']
		self.rcon2        = ['04', '00', '00', '00']
		self.rcon3        = ['08', '00', '00', '00']
		self.rcon4        = ['10', '00', '00', '00']
		self.rcon5        = ['20', '00', '00', '00']
		self.rcon6        = ['40', '00', '00', '00']
		self.rcon7        = ['80', '00', '00', '00']
		self.rcon8        = ['1b', '00', '00', '00']
		self.rcon9        = ['36', '00', '00', '00']
		self.rcon10       = ['6c', '00', '00', '00']
		self.rcon11       = ['d8', '00', '00', '00']
		self.rcon12       = ['ab', '00', '00', '00']
		self.rcon13       = ['4d', '00', '00', '00']
		# self.rcon14       = ['9a', '00', '00', '00']

		self.matrix_0     = ['02', '03', '01', '01']
		self.matrix_1     = ['01', '02', '03', '01']
		self.matrix_2     = ['01', '01', '02', '03']
		self.matrix_3     = ['03', '01', '01', '02']


		self.inv_matrix_0 = ['0e', '0b', '0d', '09']
		self.inv_matrix_1 = ['09', '0e', '0b', '0d']
		self.inv_matrix_2 = ['0d', '09', '0e', '0b']
		self.inv_matrix_3 = ['0b', '0d', '09', '0e']


	def Text_Expansion(self, text, mode):
		texts = []
		if mode == 'encrypt':
			# clear_text = text+':'
			clear_text = text
			if len(text) < 16:
				while len(clear_text)%16 != 0:
					clear_text += ' ' 
				texts.append(clear_text)

			else:
				number_of_blocks = len(clear_text)/16 + 1
				x = 0
				number = 16
				for i in range(number_of_blocks):
					texts.append(clear_text[x:number])
					x = number
					number +=16

				last_text = texts[-1]	
				if len(last_text) < 16:
					while len(last_text)%16 != 0:
						last_text += ' ' 
				texts.pop(-1)
				texts.append(last_text)
		elif mode == 'decrypt':
			number_of_blocks = len(text)/16
			x = 0
			number = 16
			for i in range(number_of_blocks):
				texts.append(text[x:number])
				x = number
				number +=16
		else:
			print '[-] You did not define the mode you want ("encrypt/decrypt")'
			sys.exit()
		return texts

	def Matrix_text(self, text):
		column_0 = []
		column_1 = []
		column_2 = []
		column_3 = []
		i = 0
		for letter in text:
			column_name = 'column_{}'.format(i)
			list_column = vars()[column_name]
			list_column.append(letter.encode('hex'))
			if len(list_column) ==4:
				i+=1
		return column_0, column_1, column_2, column_3

	
	def xor(self, column_0, column_1):
		column = []
		for i in range(4):
			int_value_1 = ord(str(column_0[i]).decode('hex'))
			int_value_2 = ord(str(column_1[i]).decode('hex'))
			xor = int_value_1^int_value_2 
			character_xor = chr(xor)
			hex_xor = character_xor.encode('hex')
			column.append(hex_xor)
		return column

	def Key_Expansion(self, secret_key, bit):
		if len(secret_key) > 16 and bit == 128:
			print Fore.RED+'[-] Secret Key: "{}" with length "{}" bytes, must be less than 16 bytes, if you want to use 128 bit encryption'.format(secret_key, str(len(secret_key)))
			sys.exit()
		elif len(secret_key) > 32:
			print Fore.RED+'[-] Secret Key: "{}" with length "{}" bytes, must be 32 bytes or less, if you want to use AES encryption'.format(secret_key, str(len(secret_key)))
			sys.exit()
		elif bit == 128: byte = 16
		elif bit == 192: byte = 24
		elif bit == 256: byte = 32
		else: 
			print Fore.RED+'Bits must be: "128", "192", "256"'
			sys.exit()
		
		if len(secret_key) != byte:
			print Fore.RED+'[-] The secret key: "{}" with length "{}" bytes, must have {} byte length'.format(secret_key, str(len(secret_key)), byte)
			sys.exit()

		if bit == 128:
			return secret_key
		elif bit == 192:
			secret_key += '        '

		secret_key_0 =  secret_key[:16]
		secret_key_1 =  secret_key[16:32]
		sec_key_0 = aes.Matrix_text(secret_key_0)
		sec_key_1 = aes.Matrix_text(secret_key_1)
		secret_key = ''
		for i in range(4):
			key_list = aes.xor(sec_key_0[i], sec_key_1[i])
			for k in key_list:
				secret_key +=chr(ord(k.decode('hex')))
		return secret_key

	def Hex_to_Int(self, hex_letter):
		try:
			hex_letter_0 = int(hex_letter[0])
		except ValueError:	
			if   hex_letter[0] == 'a':  hex_letter_0 = 10
			elif hex_letter[0] == 'b':  hex_letter_0 = 11
			elif hex_letter[0] == 'c':  hex_letter_0 = 12
			elif hex_letter[0] == 'd':  hex_letter_0 = 13
			elif hex_letter[0] == 'e':  hex_letter_0 = 14
			elif hex_letter[0] == 'f':  hex_letter_0 = 15
		try:
			hex_letter_1 = int(hex_letter[1])
		except ValueError:
			if   hex_letter[1] == 'a':  hex_letter_1 = 10
			elif hex_letter[1] == 'b':  hex_letter_1 = 11
			elif hex_letter[1] == 'c':  hex_letter_1 = 12
			elif hex_letter[1] == 'd':  hex_letter_1 = 13
			elif hex_letter[1] == 'e':  hex_letter_1 = 14
			elif hex_letter[1] == 'f':  hex_letter_1 = 15
		finally:
			self.hex_letter_0 = hex_letter_0
			self.hex_letter_1 = hex_letter_1

	def Sub(self):
		if self.hex_letter_0  == 0:	
			sbcol0  =  ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76']
			return sbcol0[self.hex_letter_1]
		elif self.hex_letter_0  == 1:
			sbcol1  =  ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0']
			return sbcol1[self.hex_letter_1]
		elif self.hex_letter_0  == 2:
			sbcol2  =  ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15']
			return sbcol2[self.hex_letter_1]
		elif self.hex_letter_0  == 3:
			sbcol3  =  ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75']
			return sbcol3[self.hex_letter_1]
		elif self.hex_letter_0  == 4:
			sbcol4  =  ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84']
			return sbcol4[self.hex_letter_1]
		elif self.hex_letter_0  == 5:
			sbcol5  =  ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf']
			return sbcol5[self.hex_letter_1]
		elif self.hex_letter_0  == 6:
			sbcol6  =  ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8']
			return sbcol6[self.hex_letter_1]
		elif self.hex_letter_0  == 7:
			sbcol7  =  ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2']
			return sbcol7[self.hex_letter_1]
		elif self.hex_letter_0  == 8:
			sbcol8  =  ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73']
			return sbcol8[self.hex_letter_1]
		elif self.hex_letter_0  == 9:
			sbcol9  =  ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db']
			return sbcol9[self.hex_letter_1]
		elif self.hex_letter_0  == 10:
			sbcol10 =  ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79']
			return sbcol10[self.hex_letter_1]
		elif self.hex_letter_0  == 11:
			sbcol11 =  ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08']
			return sbcol11[self.hex_letter_1]
		elif self.hex_letter_0  == 12:
			sbcol12 =  ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a']
			return sbcol12[self.hex_letter_1]
		elif self.hex_letter_0  == 13:
			sbcol13 =  ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e']
			return sbcol13[self.hex_letter_1]
		elif self.hex_letter_0  == 14:
			sbcol14 =  ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df']
			return sbcol14[self.hex_letter_1]
		elif self.hex_letter_0  == 15:
			sbcol15 =  ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54' ,'bb', '16']
			return sbcol15[self.hex_letter_1]

	def InvSub(self, hex_letter):
		try:
			hex_letter_0 = int(hex_letter[0])
		except ValueError:	
			if   hex_letter[0] == 'a':  hex_letter_0 = 10
			elif hex_letter[0] == 'b':  hex_letter_0 = 11
			elif hex_letter[0] == 'c':  hex_letter_0 = 12
			elif hex_letter[0] == 'd':  hex_letter_0 = 13
			elif hex_letter[0] == 'e':  hex_letter_0 = 14
			elif hex_letter[0] == 'f':  hex_letter_0 = 15
		try:
			hex_letter_1 = int(hex_letter[1])
		except ValueError:
			if   hex_letter[1] == 'a':  hex_letter_1 = 10
			elif hex_letter[1] == 'b':  hex_letter_1 = 11
			elif hex_letter[1] == 'c':  hex_letter_1 = 12
			elif hex_letter[1] == 'd':  hex_letter_1 = 13
			elif hex_letter[1] == 'e':  hex_letter_1 = 14
			elif hex_letter[1] == 'f':  hex_letter_1 = 15
		finally:
			self.hex_letter_0 = hex_letter_0
			self.hex_letter_1 = hex_letter_1

		if self.hex_letter_0  == 0:	
			sbcol0  =  ['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40',	'a3', '9e', '81', 'f3', 'd7', 'fb']
			return sbcol0[self.hex_letter_1]
		elif self.hex_letter_0  == 1:
			sbcol1  =  ['7c', 'e3', '39', '82',	'9b', '2f',	'ff', '87',	'34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb']
			return sbcol1[self.hex_letter_1]
		elif self.hex_letter_0  == 2:
			sbcol2  =  ['54', '7b','94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e']
			return sbcol2[self.hex_letter_1]
		elif self.hex_letter_0  == 3:
			sbcol3  =  ['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25']
			return sbcol3[self.hex_letter_1]
		elif self.hex_letter_0  == 4:
			sbcol4  =  ['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92']
			return sbcol4[self.hex_letter_1]
		elif self.hex_letter_0  == 5:
			sbcol5  =  ['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84']
			return sbcol5[self.hex_letter_1]
		elif self.hex_letter_0  == 6:
			sbcol6  =  ['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06']
			return sbcol6[self.hex_letter_1]
		elif self.hex_letter_0  == 7:
			sbcol7  =  ['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b']
			return sbcol7[self.hex_letter_1]
		elif self.hex_letter_0  == 8:
			sbcol8  =  ['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73']
			return sbcol8[self.hex_letter_1]
		elif self.hex_letter_0  == 9:
			sbcol9  =  ['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e']
			return sbcol9[self.hex_letter_1]
		elif self.hex_letter_0  == 10:
			sbcol10 =  ['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b']
			return sbcol10[self.hex_letter_1]
		elif self.hex_letter_0  == 11:
			sbcol11 =  ['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4']
			return sbcol11[self.hex_letter_1]
		elif self.hex_letter_0  == 12:
			sbcol12 =  ['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12',	'10', '59', '27', '80', 'ec', '5f']
			return sbcol12[self.hex_letter_1]
		elif self.hex_letter_0  == 13:
			sbcol13 =  ['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef']
			return sbcol13[self.hex_letter_1]
		elif self.hex_letter_0  == 14:
			sbcol14 =  ['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61']
			return sbcol14[self.hex_letter_1]
		elif self.hex_letter_0  == 15:
			sbcol15 =  ['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']
			return sbcol15[self.hex_letter_1]

	def Rot_column_3(self, sec_key_3):
		rot_column_3 = []
		rot_column_3.append(sec_key_3[1])
		rot_column_3.append(sec_key_3[2])
		rot_column_3.append(sec_key_3[3])
		rot_column_3.append(sec_key_3[0])
		return rot_column_3

	def Rcon(self, i):
		if i == 0 : return self.rcon0
		if i == 1 : return self.rcon1
		if i == 2 : return self.rcon2
		if i == 3 : return self.rcon3
		if i == 4 : return self.rcon4
		if i == 5 : return self.rcon5
		if i == 6 : return self.rcon6
		if i == 7 : return self.rcon7
		if i == 8 : return self.rcon8
		if i == 9 : return self.rcon9
		if i == 10: return self.rcon10
		if i == 11: return self.rcon11
		if i == 12: return self.rcon12
		if i == 13: return self.rcon13
		# if i == 14: return self.rcon14

	def Key_Schedule(self, secret_key, bit, rounds):
		secret_key_0, secret_key_1, secret_key_2,  secret_key_3  = [], [], [], []
		secret_key_4, secret_key_5, secret_key_6,  secret_key_7  = [], [], [], []
		secret_key_8, secret_key_9, secret_key_10, secret_key_11 = [], [], [], []
		secret_key_12, secret_key_13, secret_key_14              = [], [], []

		for i in range(rounds):
			if i == 0:
				sec_key = aes.Matrix_text(secret_key)
				sec_key_0, sec_key_1 = sec_key[0], sec_key[1], 
				sec_key_2, sec_key_3_temp = sec_key[2], sec_key[3]
				# sec_key_0, sec_key_1, sec_key_2, sec_key_3_temp = ['2b', '7e', '15', '16'], ['28', 'ae', 'd2', 'a6'], ['ab', 'f7', '15', '88'], ['09', 'cf', '4f', '3c']
			
			sec_key_3 = aes.Rot_column_3(sec_key_3_temp)

			temp_list = []
			for x in range(len(sec_key_3)):
				new_sec_key_3     = aes.Hex_to_Int(sec_key_3[x])
				sub_new_sec_key_3 = aes.Sub()
				temp_list.append(sub_new_sec_key_3)

			key_0 = aes.xor(aes.xor(sec_key_0, temp_list), aes.Rcon(i))
			sec_key_0 = key_0
			sec_key_1 = aes.xor(sec_key_0, sec_key_1)
			sec_key_2 = aes.xor(sec_key_1, sec_key_2)
			sec_key_3 = aes.xor(sec_key_2, sec_key_3_temp)
			sec_key_3_temp = sec_key_3
			column_name = 'secret_key_{}'.format(i)
			list_column = vars()[column_name]
			list_column.append([sec_key_0, sec_key_1, sec_key_2, sec_key_3])
		
		if bit == 128: return (
								secret_key_0,  secret_key_1,  secret_key_2,  secret_key_3,  
								secret_key_4,  secret_key_5,  secret_key_6,  secret_key_7,  
								secret_key_8,  secret_key_9
							)
		elif bit == 192: return (
								secret_key_0,  secret_key_1,  secret_key_2,   secret_key_3,  
								secret_key_4,  secret_key_5,  secret_key_6,   secret_key_7,  
								secret_key_8,  secret_key_9,  secret_key_10,  secret_key_11
							)
		elif bit == 256: return (
								secret_key_0,  secret_key_1,  secret_key_2,   secret_key_3,  
								secret_key_4,  secret_key_5,  secret_key_6,   secret_key_7,  
								secret_key_8,  secret_key_9,  secret_key_10,  secret_key_11,
								secret_key_12, secret_key_13
							)
	def L_Table(self, hex_letter):
		try:
			hex_letter_0 = int(hex_letter[0])
		except ValueError:	
			if   hex_letter[0] == 'a':  hex_letter_0 = 10
			elif hex_letter[0] == 'b':  hex_letter_0 = 11
			elif hex_letter[0] == 'c':  hex_letter_0 = 12
			elif hex_letter[0] == 'd':  hex_letter_0 = 13
			elif hex_letter[0] == 'e':  hex_letter_0 = 14
			elif hex_letter[0] == 'f':  hex_letter_0 = 15
		try:
			hex_letter_1 = int(hex_letter[1])
		except ValueError:
			if   hex_letter[1] == 'a':  hex_letter_1 = 10
			elif hex_letter[1] == 'b':  hex_letter_1 = 11
			elif hex_letter[1] == 'c':  hex_letter_1 = 12
			elif hex_letter[1] == 'd':  hex_letter_1 = 13
			elif hex_letter[1] == 'e':  hex_letter_1 = 14
			elif hex_letter[1] == 'f':  hex_letter_1 = 15
		finally:
			self.hex_letter_0 = hex_letter_0
			self.hex_letter_1 = hex_letter_1


		if self.hex_letter_0  == 0:	
			sbcol0 = ['', '00', '19', '01', '32', '02', '1a', 'c6', '4b', 'c7', '1b', '68', '33', 'ee', 'df', '03']
			return ord(str(sbcol0[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 1:
			sbcol1 = ['64', '04', 'e0', '0e', '34', '8d', '81', 'ef', '4c', '71', '08', 'c8', 'f8', '69', '1c', 'c1']
			return ord(str(sbcol1[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 2:
			sbcol2 = ['7d', 'c2', '1d', 'b5', 'f9', 'b9', '27', '6a', '4d', 'e4', 'a6', '72', '9a', 'c9', '09', '78']
			return ord(str(sbcol2[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 3:
			sbcol3 = ['65', '2f', '8a', '05', '21', '0f', 'e1', '24', '12', 'f0', '82', '45', '35', '93', 'da', '8e']
			return ord(str(sbcol3[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 4:
			sbcol4 = ['96', '8f', 'db', 'bd', '36', 'd0', 'ce', '94', '13', '5c', 'd2', 'f1', '40', '46', '83', '38']
			return ord(str(sbcol4[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 5:
			sbcol5 = ['66', 'dd', 'fd', '30', 'bf', '06', '8b', '62', 'b3', '25', 'e2', '98', '22', '88', '91', '10']
			return ord(str(sbcol5[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 6:
			sbcol6 = ['7e', '6e', '48', 'c3', 'a3', 'b6', '1e', '42', '3a', '6b', '28', '54', 'fa', '85', '3d', 'ba']
			return ord(str(sbcol6[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 7:
			sbcol7 = ['2b', '79', '0a', '15', '9b', '9f', '5e', 'ca', '4e', 'd4', 'ac', 'e5', 'f3', '73', 'a7', '57']
			return ord(str(sbcol7[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 8:
			sbcol8 = ['af', '58', 'a8', '50', 'f4', 'ea', 'd6', '74', '4f', 'ae', 'e9', 'd5', 'e7', 'e6', 'ad', 'e8']
			return ord(str(sbcol8[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 9:
			sbcol9 = ['2c', 'd7', '75', '7a', 'eb', '16', '0b', 'f5', '59', 'cb', '5f', 'b0', '9c', 'a9', '51', 'a0']
			return ord(str(sbcol9[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 10:
			sbcol10 = ['7f', '0c', 'f6', '6f', '17', 'c4', '49', 'ec', 'd8', '43', '1f', '2d', 'a4', '76', '7b', 'b7']
			return ord(str(sbcol10[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 11:
			sbcol11 = ['cc', 'bb', '3e', '5a', 'fb', '60', 'b1', '86', '3b', '52', 'a1', '6c', 'aa', '55', '29', '9d']
			return ord(str(sbcol11[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 12:
			sbcol12 = ['97', 'b2', '87', '90', '61', 'be', 'dc', 'fc', 'bc', '95', 'cf', 'cd', '37', '3f', '5b', 'd1']
			return ord(str(sbcol12[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 13:
			sbcol13 = ['53', '39', '84', '3c', '41', 'a2', '6d', '47', '14', '2a', '9e', '5d', '56', 'f2', 'd3', 'ab']
			return ord(str(sbcol13[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 14:
			sbcol14 = ['44', '11', '92', 'd9', '23', '20', '2e', '89', 'b4', '7c', 'b8', '26', '77', '99', 'e3', 'a5']
			return ord(str(sbcol14[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 15:
			sbcol15 = ['67', '4a', 'ed', 'de', 'c5', '31', 'fe', '18', '0d', '63', '8c', '80', 'c0', 'f7', '70', '07']
			return ord(str(sbcol15[self.hex_letter_1].decode('hex')))

	def E_Table(self, hex_letter):
		try:
			hex_letter_0 = int(hex_letter[0])
		except ValueError:	
			if   hex_letter[0] == 'a':  hex_letter_0 = 10
			elif hex_letter[0] == 'b':  hex_letter_0 = 11
			elif hex_letter[0] == 'c':  hex_letter_0 = 12
			elif hex_letter[0] == 'd':  hex_letter_0 = 13
			elif hex_letter[0] == 'e':  hex_letter_0 = 14
			elif hex_letter[0] == 'f':  hex_letter_0 = 15
		try:
			hex_letter_1 = int(hex_letter[1])
		except ValueError:
			if   hex_letter[1] == 'a':  hex_letter_1 = 10
			elif hex_letter[1] == 'b':  hex_letter_1 = 11
			elif hex_letter[1] == 'c':  hex_letter_1 = 12
			elif hex_letter[1] == 'd':  hex_letter_1 = 13
			elif hex_letter[1] == 'e':  hex_letter_1 = 14
			elif hex_letter[1] == 'f':  hex_letter_1 = 15
		finally:
			self.hex_letter_0 = hex_letter_0
			self.hex_letter_1 = hex_letter_1


		if self.hex_letter_0  == 0:	
			sbcol0 = ['01', '03', '05', '0f', '11', '33', '55', 'ff', '1a', '2e', '72', '96', 'a1', 'f8', '13', '35']
			return ord(str(sbcol0[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 1:
			sbcol1 = ['5f', 'e1', '38', '48', 'd8', '73', '95', 'a4', 'f7', '02', '06', '0a', '1e', '22', '66', 'aa']
			return ord(str(sbcol1[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 2:
			sbcol2 = ['e5', '34', '5c', 'e4', '37', '59', 'eb', '26', '6a', 'be', 'd9', '70', '90', 'ab', 'e6', '31']
			return ord(str(sbcol2[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 3:
			sbcol3 = ['53', 'f5', '04', '0c', '14', '3c', '44', 'cc', '4f', 'd1', '68', 'b8', 'd3', '6e', 'b2', 'cd']
			return ord(str(sbcol3[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 4:
			sbcol4 = ['4c', 'd4', '67', 'a9', 'e0', '3b', '4d', 'd7', '62', 'a6', 'f1', '08', '18', '28', '78', '88']
			return ord(str(sbcol4[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 5:
			sbcol5 = ['83', '9e', 'b9', 'd0', '6b', 'bd', 'dc', '7f', '81', '98', 'b3', 'ce', '49', 'db', '76', '9a']
			return ord(str(sbcol5[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 6:
			sbcol6 = ['b5', 'c4', '57', 'f9', '10', '30', '50', 'f0', '0b', '1d', '27', '69', 'bb', 'd6', '61', 'a3']
			return ord(str(sbcol6[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 7:
			sbcol7 = ['fe', '19', '2b', '7d', '87', '92', 'ad', 'ec', '2f', '71', '93', 'ae', 'e9', '20', '60', 'a0']
			return ord(str(sbcol7[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 8:
			sbcol8 = ['fb', '16', '3a', '4e' ,'d2', '6d', 'b7', 'c2', '5d', 'e7', '32', '56', 'fa', '15', '3f', '41']
			return ord(str(sbcol8[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 9:
			sbcol9 = ['c3', '5e', 'e2', '3d', '47', 'c9', '40', 'c0', '5b', 'ed', '2c', '74', '9c', 'bf', 'da', '75']
			return ord(str(sbcol9[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 10:
			sbcol10 = ['9f', 'ba', 'd5', '64', 'ac', 'ef', '2a', '7e', '82', '9d', 'bc', 'df', '7a', '8e', '89', '80']
			return ord(str(sbcol10[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 11:
			sbcol11 = ['9b', 'b6', 'c1', '58', 'e8', '23', '65', 'af', 'ea', '25', '6f', 'b1', 'c8', '43', 'c5', '54']
			return ord(str(sbcol11[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 12:
			sbcol12 = ['fc', '1f', '21', '63', 'a5', 'f4', '07', '09', '1b', '2d', '77', '99', 'b0', 'cb', '46', 'ca']
			return ord(str(sbcol12[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 13:
			sbcol13 = ['45', 'cf', '4a', 'de', '79', '8b', '86', '91', 'a8', 'e3', '3e', '42', 'c6', '51', 'f3', '0e']
			return ord(str(sbcol13[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 14:
			sbcol14 = ['12', '36', '5a', 'ee', '29', '7b', '8d', '8c', '8f', '8a', '85', '94', 'a7', 'f2', '0d', '17']
			return ord(str(sbcol14[self.hex_letter_1].decode('hex')))
		elif self.hex_letter_0  == 15:
			sbcol15 = ['39', '4b', 'dd', '7c', '84', '97', 'a2', 'fd', '1c', '24', '6c', 'b4', 'c7', '52', 'f6', '01']
			return ord(str(sbcol15[self.hex_letter_1].decode('hex')))

	def Hex(self, element):
		if element >255: 
			element -= 255 
		element = chr(element).encode('hex')
		self.element = element
		return self.element

	def InvMix_Col(self, column):
		new_column = []
		for i in range(len(column)):
			if   i == 0: inv_matrix = self.inv_matrix_0
			elif i == 1: inv_matrix = self.inv_matrix_1
			elif i == 2: inv_matrix = self.inv_matrix_2
			elif i == 3: inv_matrix = self.inv_matrix_3

			if column[0] != '00':
				element0L0 = aes.L_Table(column[0]) + aes.L_Table(inv_matrix[0])
				element0L0 = aes.Hex(element0L0)
				element0E0 = aes.E_Table(element0L0)
				# element0E0 = aes.Hex(element0E0)
			else:
				element0E0 = 0

			if column[1] != '00':
				element0L1 = aes.L_Table(column[1]) + aes.L_Table(inv_matrix[1])
				element0L1 = aes.Hex(element0L1)
				element0E1 = aes.E_Table(element0L1)
				# element0E1 = aes.Hex(element0E1)
			else:
				element0E1 = 0

			if column[2] != '00':
				element0L2 = aes.L_Table(column[2]) + aes.L_Table(inv_matrix[2])
				element0L2 = aes.Hex(element0L2)
				element0E2 = aes.E_Table(element0L2)
				# element0E2 = aes.Hex(element0E2)
			else:
				element0E2 = 0

			if column[3] != '00':
				element0L3 = aes.L_Table(column[3]) + aes.L_Table(inv_matrix[3])
				element0L3 = aes.Hex(element0L3)
				element0E3 = aes.E_Table(element0L3)
				# element0E3 = aes.Hex(element0E3)
			else:
				element0E3 = 0
			element0 = chr(element0E0 ^ element0E1 ^ element0E2 ^ element0E3).encode('hex')
			new_column.append(element0)
		
		return new_column

	def Mix_Col(self, column):

		new_column = []
		for i in range(len(column)):
			if   i == 0: matrix = self.matrix_0
			elif i == 1: matrix = self.matrix_1
			elif i == 2: matrix = self.matrix_2
			elif i == 3: matrix = self.matrix_3
			
			if column[0] != '00':
				element0L0 = aes.L_Table(column[0]) + aes.L_Table(matrix[0])
				element0L0 = aes.Hex(element0L0)
				element0E0 = aes.E_Table(element0L0)
			else: element0E0 = 0

			if column[1] != '00': 
				element0L1 = aes.L_Table(column[1]) + aes.L_Table(matrix[1])
				element0L1 = aes.Hex(element0L1)
				element0E1 = aes.E_Table(element0L1)
			else: element0E1 = 0
			
			if column[2] != '00':
				element0L2 = aes.L_Table(column[2]) + aes.L_Table(matrix[2]) ##bug for column = ['7e', '4a', '00', 'b6'] and matrix = ['02', '03', '01', '01']
				element0L2 = aes.Hex(element0L2)
				element0E2 = aes.E_Table(element0L2)
			else: element0E2 = 0
			
			if column[3] != '00':	
				element0L3 = aes.L_Table(column[3]) + aes.L_Table(matrix[3])
				element0L3 = aes.Hex(element0L3)
				element0E3 = aes.E_Table(element0L3)
			else: element0E3 = 0
			
			element0 = chr(element0E0 ^ element0E1 ^ element0E2 ^ element0E3).encode('hex')
			new_column.append(element0)
		
		return new_column	

	def AddRoundKey(self, secret_key, text):
		new_text = []
		for i in range(4):
			t = aes.xor(secret_key[i], text[i])
			new_text.append(t)
		return new_text

	def SubBytes(self, new_text):
		text_0 = []
		text_1 = []
		text_2 = []
		text_3 = []
		i = 0
		for text in new_text:
			for t in text:
				letter      = aes.Hex_to_Int(t)
				new_letter  = aes.Sub()
				column_name = 'text_{}'.format(i)
				list_column = vars()[column_name]
				list_column.append(new_letter)
			i+=1
		return text_0 ,text_1, text_2, text_3 

	def InvSubBytes(self, new_text):
		text_0 = []
		text_1 = []
		text_2 = []
		text_3 = []
		i = 0
		for text in new_text:
			for t in text:
				new_letter  = aes.InvSub(t)
				column_name = 'text_{}'.format(i)
				list_column = vars()[column_name]
				list_column.append(new_letter)
			i+=1
		return text_0 ,text_1, text_2, text_3 

	def ShiftRows(self, subed_text):
		subed_text_0     = subed_text[0]
		subed_text_1     = subed_text[1]
		subed_text_2     = subed_text[2]
		subed_text_3     = subed_text[3]

		new_column_0     = [subed_text_0[0], subed_text_1[0], subed_text_2[0], subed_text_3[0]]
		new_column_1     = [subed_text_0[1], subed_text_1[1], subed_text_2[1], subed_text_3[1]]
		new_column_2     = [subed_text_0[2], subed_text_1[2], subed_text_2[2], subed_text_3[2]]
		new_column_3     = [subed_text_0[3], subed_text_1[3], subed_text_2[3], subed_text_3[3]]
		
		shifted_column_0 =  new_column_0
		shifted_column_1 = [new_column_1[1], new_column_1[2], new_column_1[3], new_column_1[0]]
		shifted_column_2 = [new_column_2[2], new_column_2[3], new_column_2[0], new_column_2[1]]
		shifted_column_3 = [new_column_3[3], new_column_3[0], new_column_3[1], new_column_3[2]]
		
		column_0         = [shifted_column_0[0], shifted_column_1[0], shifted_column_2[0], shifted_column_3[0]]
		column_1         = [shifted_column_0[1], shifted_column_1[1], shifted_column_2[1], shifted_column_3[1]]
		column_2         = [shifted_column_0[2], shifted_column_1[2], shifted_column_2[2], shifted_column_3[2]]
		column_3         = [shifted_column_0[3], shifted_column_1[3], shifted_column_2[3], shifted_column_3[3]]

		return column_0, column_1, column_2, column_3


	def InvShiftRows(self, subed_text):
		subed_text_0 = subed_text[0]
		subed_text_1 = subed_text[1]
		subed_text_2 = subed_text[2]
		subed_text_3 = subed_text[3]

		column_0 = [subed_text_0[0], subed_text_3[1], subed_text_2[2], subed_text_1[3]]
		column_1 = [subed_text_1[0], subed_text_0[1], subed_text_3[2], subed_text_2[3]]
		column_2 = [subed_text_2[0], subed_text_1[1], subed_text_0[2], subed_text_3[3]]
		column_3 = [subed_text_3[0], subed_text_2[1], subed_text_1[2], subed_text_0[3]]
		
		return column_0, column_1, column_2, column_3

	def MixColumns(self, shifted_text):
		mixed_column_0 = aes.Mix_Col(shifted_text[0])
		mixed_column_1 = aes.Mix_Col(shifted_text[1])
		mixed_column_2 = aes.Mix_Col(shifted_text[2])
		mixed_column_3 = aes.Mix_Col(shifted_text[3])
		return mixed_column_0, mixed_column_1, mixed_column_2, mixed_column_3

	def InvMixColumns(self, shifted_text):
		mixed_column_0 = aes.InvMix_Col(shifted_text[0])
		mixed_column_1 = aes.InvMix_Col(shifted_text[1])
		mixed_column_2 = aes.InvMix_Col(shifted_text[2])
		mixed_column_3 = aes.InvMix_Col(shifted_text[3])
		return mixed_column_0, mixed_column_1, mixed_column_2, mixed_column_3


	def Encrypt(self, clear_text, secret_key, bit):
		cipher_list = []
		secret_key  = aes.Key_Expansion(secret_key, bit)               #returns an 128 bit secret key
		clear_text  = aes.Text_Expansion(clear_text, 'encrypt')        #returns a list with clear text

		if    bit == 128: rounds = 10
		elif  bit == 192: rounds = 12
		elif  bit == 256: rounds = 14

		secret_key_matrix = aes.Matrix_text(secret_key)
		keys              = aes.Key_Schedule(secret_key, bit, rounds)  #returns a list of all keys
		
		for state in clear_text:
			text = aes.Matrix_text(state)
			text = text[0], text[1], text[2], text[3]
			print 'Matrix Text: '+ str(text)

			add_r =  aes.AddRoundKey(secret_key_matrix, text)
			print 'AddRoundKey: {} xor {} ---> {}'.format(str(secret_key_matrix), str(text), str(add_r))
			print ''
			for r in range(rounds):
				print Fore.YELLOW + 'Round: ' + str(r)
				subed_text   = aes.SubBytes(add_r)
				print 'SubeBytes: {} ---> {}'.format(str(add_r), str(subed_text))
				shifted_text = aes.ShiftRows(subed_text)
				print 'ShiftRows: {} ---> {}'.format(str(subed_text), str(shifted_text))
				mix_text     = aes.MixColumns(shifted_text)
				print 'MixColumns: {} ---> {}'.format(str(shifted_text), str(mix_text))
				add_r        =  aes.AddRoundKey(keys[r][0], mix_text)
				print 'AddRoundKey: {} xor {} ---> {}'.format(str(keys[r][0]), str(mix_text), str(add_r))
				# print 'AddRoundKey: '+str(keys[r][0]) +' xor ' str(mix_text)+ ' ---> ' + str(add_r)
				print ''

			subed_text   = aes.SubBytes(add_r)
			print 'SubeBytes: {} ---> {}'.format(str(add_r), str(subed_text))
			shifted_text = aes.ShiftRows(subed_text)
			print 'ShiftRows: {} ---> {}'.format(str(subed_text), str(shifted_text))
			add_r =  aes.AddRoundKey(keys[-1][0], shifted_text)
			print 'AddRoundKey: {} xor {} ---> {}'.format(str(keys[-1][0]), str(shifted_text), str(add_r))
			# print 'AddRoundKey: '+str(keys[-1][0]) +' xor ' str(shifted_text)+ ' ---> ' + str(add_r)
			cipher_list.append(add_r)


		cipher_text = ''
		for cipher in cipher_list:
			for ci in cipher:
				for c in ci:
					cipher_text += chr(ord(c.decode('hex')))
		return cipher_text
				

	def Reversing_Keys(self, keys):

		new_keys = []
		for k in reversed(keys):
			new_keys.append(k[0])
		return new_keys

	def Decrypt(self, cipher_text, secret_key, bit):
		clear_list = []

		if    bit == 128: rounds = 10
		elif  bit == 192: rounds = 12
		elif  bit == 256: rounds = 14

		
		secret_key        = aes.Key_Expansion(secret_key, bit)         #returns an 128 bit secret key
		secret_key_matrix = aes.Matrix_text(secret_key)                #returns the original secret key in 4x4 matrix
		keys              = aes.Key_Schedule(secret_key, bit, rounds)  #returns a list of all keys
		keys              = aes.Reversing_Keys(keys)

		cipher_text       = aes.Text_Expansion(cipher_text,'decrypt')  #returns a list with cipher text
		
		for cipher in cipher_text:
			text = aes.Matrix_text(cipher)
			text = text[0], text[1], text[2], text[3]
			print 'Matrix Text: '+ str(text)

			add_r =  aes.AddRoundKey(keys[0], text)
			print 'AddRoundKey: {} xor {} ---> {}'.format(str(keys[0]), str(text), str(add_r))
			print ''
			for r in range(rounds):
				print Fore.YELLOW+'Round: '+ str(r)
				shifted_text = aes.InvShiftRows(add_r)
				print 'ShiftRows: {} ---> {}'.format(str(add_r), str(shifted_text))
				subed_text   = aes.InvSubBytes(shifted_text)
				print 'SubeBytes: {} ---> {}'.format(str(shifted_text), str(subed_text))
				add_r        =  aes.AddRoundKey(keys[r], subed_text)
				print 'AddRoundKey: {} xor {} ---> {}'.format(str(keys[r]), str(subed_text), str(add_r))
				mix_text     = aes.InvMixColumns(add_r)
				print 'MixColumns: {} ---> {}'.format(str(add_r), str(mix_text))
				add_r        = mix_text
				print ''

			shifted_text = aes.InvShiftRows(add_r)
			print 'ShiftRows: {} ---> {}'.format(str(add_r), str(shifted_text))
			subed_text   = aes.InvSubBytes(shifted_text)
			print 'SubeBytes: {} ---> {}'.format(str(shifted_text), str(subed_text))
			add_r =  aes.AddRoundKey(secret_key_matrix, subed_text)
			print 'AddRoundKey: {} xor {} ---> {}'.format(str(secret_key_matrix), str(subed_text), str(add_r))
			print '\n'
			clear_list.append(add_r)

		clear_text = ''
		for clear in clear_list:
			for ci in clear:
				for c in ci:
					clear_text += chr(ord(c.decode('hex')))
		return clear_text.strip()





if __name__ == '__main__':
	try:
		init(autoreset=True)
		text = raw_input(Fore.YELLOW+'[*] Set the text you want to encrypt: '+ Style.RESET_ALL) 
		# sec_key = 'asdhjuiktu76tgb4'#16
		# bit = 128
		# sec_key = 'asdhjuiktu76tgb49olxb4Ec'#24
		# bit = 192
		# sec_key = 'asdhjuiktu76tgb49olxb4Ecsgbqus70'#32
		# bit = 256
		for i in range(3):
			try:
				bit = int(raw_input(Fore.YELLOW+'[*] Select the bit for the encryption ("128"/"192"/"256"): '+ Style.RESET_ALL))
				bit = int(bit)
				break
			except ValueError:
				print Fore.RED + '[-] bit must be an integer'
				if i == 2:
					sys.exit()
				else:
					print  Fore.YELLOW+'[*] Please try again...\n'

		sec_key =  raw_input(Fore.YELLOW+'[*] Set the secret key for encryption: '+ Style.RESET_ALL)
		if sec_key == 'random':
			characters = '~!@#$%^&*()<>?,./-=_+'
			if  bit == 128: 
				length = 16
			elif bit == 192:
				length = 24 	
			else:
				length = 32
			sec_key = "".join([random.choice(string.ascii_letters+string.digits+characters) for i in xrange(length)])

		print ''
		aes = AES()
		encrypt = aes.Encrypt(text, sec_key, bit)
		print '\n\n'+Fore.GREEN+'Cipher Text: '+ Style.RESET_ALL + encrypt

		print '\n\n\n'
		print Fore.YELLOW+'[*] Decrypting  '+ Fore.WHITE+ encrypt+ Fore.YELLOW+'  using as a secret key: '+Fore.WHITE+sec_key
		raw_input()
		# encrypt = raw_input(Fore.YELLOW+'[*] Set the cipher text: '+ Style.RESET_ALL)
		# sec_key = raw_input(Fore.YELLOW+'[*] Set the secret key for decryption: '+ Style.RESET_ALL)
		decrypt = aes.Decrypt(encrypt, sec_key, bit)
		print '\n\n'+ Fore.GREEN +'Clear Text: '+ Style.RESET_ALL +decrypt
		raw_input()

	except Exception as e:
		print Fore.RED + '[-]'+str(e)

	except KeyboardInterrupt:
		sys.exit()