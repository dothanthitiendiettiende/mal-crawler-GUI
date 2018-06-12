rule test
{
	strings:
		$stub = "This program cannot be run in DOS mode"
	condition:
		(uint16(0) == 0x5A4D or $stub)
}