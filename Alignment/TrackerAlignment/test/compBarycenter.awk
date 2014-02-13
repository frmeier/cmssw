
BEGIN {
	FS=",";
	N1=0;
	x1=0;
	y1=0;
	N2=0;
	z1=0;
	x2=0;
	y2=0;
	z2=0;
}

/^</ {
	x1+=$7;
	y1+=$8;
	z1+=$9;
	N1++;
}

/^>/ {
	x2+=$7;
	y2+=$8;
	z2+=$9;
	N2++;
}

END {
	f=10000;
	printf "            N     x µm     y µm     z µm\n";
	printf "<    %8d %8.4f %8.4f %8.4f \n", N1, x1/N1*f, y1/N1*f, z1/N1*f;
	printf ">    %8d %8.4f %8.4f %8.4f \n", N2, x2/N2*f, y2/N2*f, z2/N2*f;
	printf "Diff %8d %8.4f %8.4f %8.4f \n",  N2-N1, x2*f/N2-x1*f/N1, y2*f/N2-y1*f/N1, z2*f/N2-z1*f/N1;
}

