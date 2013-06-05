SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
SELECT DropGeometryColumn('','train_williamstown','geom');
DROP TABLE "train_williamstown";
BEGIN;
CREATE TABLE "train_williamstown" (gid serial,
"name" varchar(80),
"descriptio" varchar(254),
"timestamp" date,
"begin" date,
"end" date,
"altitudemo" varchar(80),
"tessellate" numeric(10,0),
"extrude" numeric(10,0),
"visibility" numeric(10,0),
"draworder" numeric(10,0),
"icon" varchar(80));
ALTER TABLE "train_williamstown" ADD PRIMARY KEY (gid);
SELECT AddGeometryColumn('','train_williamstown','geom','4326','LINESTRING',2);
COPY "train_williamstown" ("name","descriptio","timestamp","begin","end","altitudemo","tessellate","extrude","visibility","draworder","icon",geom) FROM stdin;
Pattern 1 (trips: 107)	Trips using this pattern (107 in total): 3010230, 3010234, 3010237, 3010239, 3010242, 3010245, 3010247, 3010250, 3010253, 3010255, 3010258, 3010261, 3010264, 3010266, 3010269, 3010272, 3010275, 3010278, 3010281, 3010284, 3010287, 3010290, 3010293, 301029	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E6100000040000001689096AF81C6240917C259012EF42C04F7633A39F1C6240952A51F696EE42C07E1EA33C731C624099F04BFDBCED42C0AC53E57B461C6240D0F0660DDEEB42C0
Pattern 2 (trips: 103)	Trips using this pattern (103 in total): 3010727, 3010730, 3010732, 3010735, 3010738, 3010741, 3010744, 3010747, 3010750, 3010753, 3010756, 3010759, 3010762, 3010765, 3010768, 3010771, 3010774, 3010777, 3010780, 3010783, 3010786, 3010789, 3010792, 301079	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000004000000AC53E57B461C6240D0F0660DDEEB42C07E1EA33C731C624099F04BFDBCED42C04F7633A39F1C6240952A51F696EE42C01689096AF81C6240917C259012EF42C0
Pattern 3 (trips: 95)	Trips using this pattern (95 in total): 3010265, 3010268, 3010271, 3010273, 3010276, 3010279, 3010282, 3010285, 3010288, 3010291, 3010294, 3010297, 3010300, 3010303, 3010306, 3010309, 3010312, 3010315, 3010318, 3010321, 3010324, 3010327, 3010330, 3010333	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000005000000317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C032056B9CCD1E624031ED9BFBABE742C09561DC0D221F6240EF2076A6D0E742C0F629C764F11E624010070951BEE842C0
Pattern 4 (trips: 93)	Trips using this pattern (93 in total): 3010751, 3010754, 3010757, 3010760, 3010763, 3010766, 3010769, 3010772, 3010775, 3010778, 3010781, 3010784, 3010787, 3010790, 3010793, 3010796, 3010799, 3010802, 3010805, 3010808, 3010811, 3010814, 3010817, 3010820	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000B00000032056B9CCD1E624031ED9BFBABE742C09561DC0D221F6240EF2076A6D0E742C0F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0C70E2A719D1D62405089EB1857E642C0317E1AF7E61C624078280AF489E642C05C02F04FA91C624035B742588DE742C02733DE567A1C6240B6BC72BD6DE842C0376C5B94591C6240DCF4673F52EA42C0AC53E57B461C6240D0F0660DDEEB42C0
Pattern 5 (trips: 92)	Trips using this pattern (92 in total): 3010267, 3010270, 3010274, 3010277, 3010280, 3010283, 3010286, 3010289, 3010292, 3010295, 3010298, 3010301, 3010304, 3010307, 3010310, 3010313, 3010316, 3010319, 3010322, 3010325, 3010328, 3010331, 3010334, 3010337	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000A000000AC53E57B461C6240D0F0660DDEEB42C0376C5B94591C6240DCF4673F52EA42C02733DE567A1C6240B6BC72BD6DE842C05C02F04FA91C624035B742588DE742C0317E1AF7E61C624078280AF489E642C0C70E2A719D1D62405089EB1857E642C06C5B94D9201E624038BC202235E742C032056B9CCD1E624031ED9BFBABE742C09561DC0D221F6240EF2076A6D0E742C0F629C764F11E624010070951BEE842C0
Pattern 6 (trips: 91)	Trips using this pattern (91 in total): 3010752, 3010755, 3010758, 3010764, 3010767, 3010770, 3010773, 3010776, 3010779, 3010782, 3010785, 3010788, 3010791, 3010794, 3010797, 3010800, 3010803, 3010806, 3010809, 3010812, 3010815, 3010818, 3010821, 3010824	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000600000032056B9CCD1E624031ED9BFBABE742C09561DC0D221F6240EF2076A6D0E742C0F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C0
Pattern 7 (trips: 49)	Trips using this pattern (49 in total): 3010067, 3010070, 3010073, 3010076, 3010122, 3010125, 3010128, 3010131, 3010134, 3010137, 3010140, 3010143, 3010146, 3010149, 3010152, 3010155, 3010158, 3010161, 3010164, 3010167, 3010170, 3010173, 3010176, 3010180	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000009000000AC53E57B461C6240D0F0660DDEEB42C0376C5B94591C6240DCF4673F52EA42C02733DE567A1C6240B6BC72BD6DE842C05C02F04FA91C624035B742588DE742C0317E1AF7E61C624078280AF489E642C0C70E2A719D1D62405089EB1857E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C0
Pattern 8 (trips: 48)	Trips using this pattern (48 in total): 3010548, 3010553, 3010556, 3010559, 3010564, 3010569, 3010575, 3010581, 3010587, 3010593, 3010598, 3010600, 3010603, 3010607, 3010610, 3010613, 3010616, 3010619, 3010622, 3010625, 3010628, 3010631, 3010634, 3010637	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000009000000F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0C70E2A719D1D62405089EB1857E642C0317E1AF7E61C624078280AF489E642C05C02F04FA91C624035B742588DE742C02733DE567A1C6240B6BC72BD6DE842C0376C5B94591C6240DCF4673F52EA42C0AC53E57B461C6240D0F0660DDEEB42C0
Pattern 9 (trips: 42)	Trips using this pattern (42 in total): 3010549, 3010551, 3010554, 3010557, 3010562, 3010567, 3010572, 3010579, 3010584, 3010590, 3010595, 3010597, 3010601, 3010605, 3010608, 3010611, 3010614, 3010617, 3010620, 3010623, 3010626, 3010629, 3010632, 3010635	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000C000000F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0C70E2A719D1D62405089EB1857E642C0317E1AF7E61C624078280AF489E642C05C02F04FA91C624035B742588DE742C02733DE567A1C6240B6BC72BD6DE842C0376C5B94591C6240DCF4673F52EA42C0AC53E57B461C6240D0F0660DDEEB42C07E1EA33C731C624099F04BFDBCED42C04F7633A39F1C6240952A51F696EE42C01689096AF81C6240917C259012EF42C0
Pattern 10 (trips: 35)	Trips using this pattern (35 in total): 3010065, 3010068, 3010071, 3010074, 3010078, 3010126, 3010129, 3010132, 3010135, 3010138, 3010141, 3010144, 3010147, 3010150, 3010153, 3010156, 3010159, 3010162, 3010165, 3010168, 3010171, 3010174, 3010178, 3010181	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000C0000001689096AF81C6240917C259012EF42C04F7633A39F1C6240952A51F696EE42C07E1EA33C731C624099F04BFDBCED42C0AC53E57B461C6240D0F0660DDEEB42C0376C5B94591C6240DCF4673F52EA42C02733DE567A1C6240B6BC72BD6DE842C05C02F04FA91C624035B742588DE742C0317E1AF7E61C624078280AF489E642C0C70E2A719D1D62405089EB1857E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C0
Pattern 11 (trips: 33)	Trips using this pattern (33 in total): 3010154, 3010157, 3010160, 3010163, 3010166, 3010169, 3010172, 3010175, 3010177, 3010179, 3010182, 3010186, 3010189, 3010191, 3010193, 3010195, 3010198, 3010202, 3010205, 3010210, 3010215, 3010218, 3010221, 3010226	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000007000000317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C09561DC0D221F6240EF2076A6D0E742C032056B9CCD1E624031ED9BFBABE742C061AA99B5941E6240278925E5EEE742C0
Pattern 12 (trips: 31)	Trips using this pattern (31 in total): 3010642, 3010645, 3010648, 3010651, 3010654, 3010660, 3010663, 3010665, 3010670, 3010672, 3010674, 3010678, 3010680, 3010683, 3010686, 3010688, 3010694, 3010699, 3010702, 3010707, 3010716, 3010720, 3010724, 3010726	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000007000000F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C09561DC0D221F6240EF2076A6D0E742C032056B9CCD1E624031ED9BFBABE742C061AA99B5941E6240278925E5EEE742C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C0
Pattern 13 (trips: 27)	Trips using this pattern (27 in total): 3010555, 3010558, 3010561, 3010566, 3010570, 3010573, 3010576, 3010578, 3010582, 3010585, 3010588, 3010591, 3010594, 3010599, 3010602, 3010604, 3010606, 3010609, 3010612, 3010615, 3010618, 3010621, 3010624, 3010627	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000700000061AA99B5941E6240278925E5EEE742C032056B9CCD1E624031ED9BFBABE742C09561DC0D221F6240EF2076A6D0E742C0F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C0
Pattern 14 (trips: 26)	Trips using this pattern (26 in total): 3010066, 3010069, 3010075, 3010077, 3010079, 3010084, 3010090, 3010092, 3010097, 3010099, 3010101, 3010106, 3010108, 3010110, 3010112, 3010117, 3010120, 3010123, 3010127, 3010130, 3010133, 3010136, 3010139, 3010142	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000007000000317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C061AA99B5941E6240278925E5EEE742C032056B9CCD1E624031ED9BFBABE742C09561DC0D221F6240EF2076A6D0E742C0F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C0
Pattern 15 (trips: 24)	Trips using this pattern (24 in total): 3010560, 3010563, 3010565, 3010568, 3010571, 3010574, 3010577, 3010580, 3010583, 3010586, 3010589, 3010592, 3010596, 3010675, 3010677, 3010681, 3010684, 3010687, 3010691, 3010693, 3010697, 3010700, 3010703, 3010705	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000006000000F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0C70E2A719D1D62405089EB1857E642C0317E1AF7E61C624078280AF489E642C0AC53E57B461C6240D0F0660DDEEB42C0
Pattern 16 (trips: 13)	Trips using this pattern (13 in total): 3010081, 3010083, 3010086, 3010089, 3010093, 3010096, 3010100, 3010104, 3010107, 3010111, 3010114, 3010116, 3010119	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000006000000AC53E57B461C6240D0F0660DDEEB42C0317E1AF7E61C624078280AF489E642C0C70E2A719D1D62405089EB1857E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C0
Pattern 17 (trips: 9)	Trips using this pattern (9 in total): 3010194, 3010199, 3010211, 3010213, 3010216, 3010220, 3010224, 3010225, 3010231	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000005000000AC53E57B461C6240D0F0660DDEEB42C0317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C0
Pattern 18 (trips: 8)	Trips using this pattern (8 in total): 3010082, 3010088, 3010095, 3010102, 3010109, 3010115, 3010121, 3010124	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000B0000001689096AF81C6240917C259012EF42C04F7633A39F1C6240952A51F696EE42C07E1EA33C731C624099F04BFDBCED42C0AC53E57B461C6240D0F0660DDEEB42C0376C5B94591C6240DCF4673F52EA42C02733DE567A1C6240B6BC72BD6DE842C05C02F04FA91C624035B742588DE742C0317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C0
Pattern 19 (trips: 7)	Trips using this pattern (7 in total): 3010550, 3010552, 3010761, 3010908, 3010910, 3010911, 3010927	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000004000000F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C0
Pattern 20 (trips: 7)	Trips using this pattern (7 in total): 3010080, 3010085, 3010091, 3010098, 3010105, 3010113, 3010118	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000008000000AC53E57B461C6240D0F0660DDEEB42C0376C5B94591C6240DCF4673F52EA42C02733DE567A1C6240B6BC72BD6DE842C05C02F04FA91C624035B742588DE742C0317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C0
Pattern 21 (trips: 7)	Trips using this pattern (7 in total): 3010639, 3010657, 3010667, 3010690, 3010696, 3010711, 3010713	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000006000000F629C764F11E624010070951BEE842C09561DC0D221F6240EF2076A6D0E742C032056B9CCD1E624031ED9BFBABE742C061AA99B5941E6240278925E5EEE742C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C0
Pattern 22 (trips: 6)	Trips using this pattern (6 in total): 3010709, 3010712, 3010715, 3010718, 3010721, 3010723	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000005000000F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C0AC53E57B461C6240D0F0660DDEEB42C0
Pattern 23 (trips: 5)	Trips using this pattern (5 in total): 3010679, 3010685, 3010692, 3010698, 3010704	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000008000000F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C05C02F04FA91C624035B742588DE742C02733DE567A1C6240B6BC72BD6DE842C0376C5B94591C6240DCF4673F52EA42C0AC53E57B461C6240D0F0660DDEEB42C0
Pattern 24 (trips: 5)	Trips using this pattern (5 in total): 3010072, 3010087, 3010094, 3010103, 3010151	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000006000000317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C061AA99B5941E6240278925E5EEE742C032056B9CCD1E624031ED9BFBABE742C09561DC0D221F6240EF2076A6D0E742C0F629C764F11E624010070951BEE842C0
Pattern 25 (trips: 5)	Trips using this pattern (5 in total): 3010676, 3010682, 3010689, 3010695, 3010701	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E61000000B000000F629C764F11E624010070951BEE842C0F7949C137B1E6240691EC022BFE842C06C5B94D9201E624038BC202235E742C0317E1AF7E61C624078280AF489E642C05C02F04FA91C624035B742588DE742C02733DE567A1C6240B6BC72BD6DE842C0376C5B94591C6240DCF4673F52EA42C0AC53E57B461C6240D0F0660DDEEB42C07E1EA33C731C624099F04BFDBCED42C04F7633A39F1C6240952A51F696EE42C01689096AF81C6240917C259012EF42C0
Pattern 26 (trips: 4)	Trips using this pattern (4 in total): 3010184, 3010262, 3010420, 3010421	\N	\N	\N	\N	1	-1	0	\N	\N	0102000020E610000004000000317E1AF7E61C624078280AF489E642C06C5B94D9201E624038BC202235E742C0F7949C137B1E6240691EC022BFE842C0F629C764F11E624010070951BEE842C0
\.
CREATE INDEX "train_williamstown_geom_gist" ON "train_williamstown" USING GIST ("geom");
COMMIT;
