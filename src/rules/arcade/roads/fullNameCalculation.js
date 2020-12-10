return iif(isempty($feature.NAME), true, Upper(Trim(Replace(Concatenate([$feature.NAME, $feature.POSTTYPE, $feature.POSTDIR], " "), "  ", " "))));
