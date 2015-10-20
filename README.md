unicafe-cli
===========

Command line interface for getting unicafe menus

usage
-----
Simple usage:	

	./unicafe.py <restaurant name>
	
	positional arguments:
		restaurant

	optional arguments:
		-h, --help            show this help message and exit
		-r restaurant [restaurant ...]
													name of restaurant
		-p [prices [prices ...]]
													only lunches in these price categories
		-o                    show business times
		-t                    only today's list
		-i                    show ingredients, use twice to show everything
		-n                    show nutrition information
		-s                    show special diet information
		-v                    show verbose information about lunches. same as -i -n

example
-------

	$ ./unicafe.py Chemicum
	Ke 18.02
		Kalapyöryköitä, sitruunakermaviilikastiketta
		Porsaswokkia
		Soijaa chilitomaattikastikkeessa
		Makrillisalaattia
		Vadelmakiisseliä, kermavaahtoa (Makeasti)
	To 19.02
		Kanapyörykät, BBQ-kastiketta
		Kala-paprikapataa
		Bataatti-papuhöystöä
		Palvikinkkusalaattia
		Juuressosekeittoa (Kevyesti)
		Ananasrahkaa (Makeasti)
	Pe 20.02
		Paistettua lohta, wasabi-majoneensia (Maukkaasti)
		Broileri-pekonihöystöä
		Chili-kasvisvuokaa
		Kaura-raparperipaistosta, vaniljakastiketta (Makeasti)

