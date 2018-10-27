stack = []
on_initial={} #key is on value
initial_top={} #value is on top of key

arm='0'




on_initial['A']='0'
on_initial['B']='A'
on_initial['C']='0'
on_initial['D']='C'

initial_top['A']='B'
initial_top['B']='0'
initial_top['C']='D'
initial_top['D']='0'


stack.append('ON C A ^ ON B D')
stack.append('ON C A')
stack.append('ON B D')

def unstack(x,y):
	stack.append('UNSTACK '+x+' '+y)
	stack.append('ARM')
	stack.append('ON '+x+' '+y)
	stack.append('CLEAR '+x)
	
	

def stack_up(x,y):
	stack.append('STACK '+x+' '+y)
	stack.append('HOLD '+x)
	stack.append('CLEAR '+y)


def pickup(x):
	stack.append('PICKUP '+x)
	stack.append('ARM')
	stack.append('ONT '+x)
	stack.append('CLEAR '+x)
	
	

def putdown(x):
	stack.append('PUTDOWN '+x)
	stack.append('HOLD '+x)


count=1
while len(stack)!=0:

	ele=stack.pop().split(" ")
	if ele[0]=='ON' and len(ele)==3:
		if on_initial[ele[1]]==ele[2]:
			continue
		else:
			stack_up(ele[1],ele[2])
			continue

	elif ele[0]=='CLEAR':
		if(initial_top[ele[1]]!='0'):
			unstack(initial_top[ele[1]],ele[1])
		else:
			continue			
	elif ele[0]=='ARM':
		if arm=='0':
			continue
		else:
			putdown(arm)
	elif ele[0]=='UNSTACK':
		on_initial[ele[1]]='0'
		initial_top[ele[2]]='0'
		arm=ele[1]
		print ("Action numeber "+str(count)+" taken = "+str(ele))
		count+=1
				
		
	elif ele[0]=='HOLD':
		if arm==ele[1]:
			continue
		else:
			pickup(ele[1])
	elif ele[0]=='PUTDOWN':
		arm='0'
		print ("Action number "+str(count)+" taken = "+str(ele))
		count=count+1
	
	elif ele[0]=='ONT':
		if(on_initial[ele[1]]=='0'):
			continue
		else :
			'''
			if initial_top[ele[1]]=='0':
				temp=on_initial[ele[1]]
				on_initial[ele[1]]='0'
				initial_top[temp]='0'
				print ("Action number "+str(count)+" taken = Bring "+str(ele[1])+"on table")
			'''
			unstack(ele[1],on_initial[ele[1]])
	elif ele[0]=='PICKUP':
		arm=ele[1]
		print ("Action number "+str(count)+" taken = "+str(ele))
		count+=1
	elif ele[0]=='STACK':
		on_initial[ele[1]]=ele[2]
		initial_top[ele[2]]=ele[1]
		arm='0'
		print ("Action number "+str(count)+" taken = "+str(ele))
		count+=1

	elif ele[0]=='ON' and len(ele)==7:
		if (on_initial[ele[1]]==ele[2] and on_initial[ele[5]]==ele[6]):
			continue
		else:
			stack.append(str(ele[0]+" "+ele[1]+" "+ele[2]+" "+ele[3]+" "+ele[4]+" "+ele[5]+" "+ele[6]))
			stack.append(str(ele[0]+" "+ele[1]+" "+ele[2]))
			stack.append(str(ele[4]+" "+ele[5]+" "+ele[6]))
			
