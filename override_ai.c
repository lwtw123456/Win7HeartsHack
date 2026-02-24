#include <stdint.h>
#include <stddef.h>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

DLL_EXPORT void* SelectCardToPass(void** ptr_array, int n) {
    int min_indices[3] = {-1, -1, -1};
    int min_remainders[3] = {13, 13, 13}; 
   
    for (int i = 0; i < 13; i++) {
        uint8_t* base = (uint8_t*)ptr_array[i];
        int value = *(int*)(base + 8);
        int remainder = value % 13;
        
        if (remainder < min_remainders[0]) {
            min_remainders[2] = min_remainders[1];
            min_indices[2] = min_indices[1];
            min_remainders[1] = min_remainders[0];
            min_indices[1] = min_indices[0];
            min_remainders[0] = remainder;
            min_indices[0] = i;
        } else if (remainder < min_remainders[1]) {
            min_remainders[2] = min_remainders[1];
            min_indices[2] = min_indices[1];
            min_remainders[1] = remainder;
            min_indices[1] = i;
        } else if (remainder < min_remainders[2]) {
            min_remainders[2] = remainder;
            min_indices[2] = i;
        }
    }
        return ptr_array[min_indices[n]];
}

DLL_EXPORT void* SelectCardToPlay(void** ptr_array, int n, int quotient, uint8_t* param_ptr)
{   
	uint8_t x = param_ptr[0];
    uint8_t y = param_ptr[1];
	
    int values[13];
    for (int i = 0; i < n; i++) {
        values[i] = *(int*)((uint8_t*)ptr_array[i] + 8);
    }
    
    int valid[13];
    int has_valid = 0;
    
    for (int i = 0; i < n; i++) {
        valid[i] = 1;
    }
    
    if (x == 1) {
        int has_zero = 0;
        int zero_idx = -1;
        for (int i = 0; i < n; i++) {
            if (values[i] == 0) {
                has_zero = 1;
                zero_idx = i;
                break;
            }
        }
        
        if (has_zero) {
            return ptr_array[zero_idx];
        }
        
        for (int i = 0; i < n; i++) {
            if (values[i] == 36 || values[i] / 13 == 3) {
                valid[i] = 0;
            }
        }
    } else if (x == 0 && y == 0) {
        for (int i = 0; i < n; i++) {
            if (values[i] / 13 == 3) {
                valid[i] = 0;
            }
        }
    }
    
    for (int i = 0; i < n; i++) {
        if (valid[i]) {
            has_valid = 1;
            break;
        }
    }
    
    int use_fallback = 0;
    if (!has_valid) {
        use_fallback = 1;
        for (int i = 0; i < n; i++) {
            valid[i] = 1;
        }
    }
    
    int best_idx = -1;
    int best_value = -1;
	int best_remainder = -1;
    
    if (!use_fallback) {
        if (quotient == 4) {
            for (int i = 0; i < n; i++) {
				int remainder = values[i] % 13;
                if (valid[i] && remainder > best_remainder) {
                    best_remainder = remainder;
                    best_idx = i;
                }
            }
        } else {
            int found_matching_quotient = 0;
            
            for (int i = 0; i < n; i++) {
                if (valid[i] && values[i] / 13 == quotient) {
                    found_matching_quotient = 1;
                    int remainder = values[i] % 13;
                    if (remainder > best_remainder) {
                        best_remainder = remainder;
                        best_idx = i;
                    }
                }
            }
            
            if (!found_matching_quotient) {
                for (int i = 0; i < n; i++) {
					int remainder = values[i] % 13;
                    if (valid[i] && remainder > best_remainder) {
                        best_remainder = remainder;
                        best_idx = i;
                    }
                }
            }
        }
    } else {
        if (quotient == 4) {
            for (int i = 0; i < n; i++) {
				int remainder = values[i] % 13;
                if (remainder > best_remainder) {
                    best_remainder = remainder;
                    best_idx = i;
                }
            }
        } else {
            int found_matching_quotient = 0;
            
            for (int i = 0; i < n; i++) {
                if (values[i] / 13 == quotient) {
                    found_matching_quotient = 1;
                    int remainder = values[i] % 13;
                    if (remainder > best_remainder) {
                        best_remainder = remainder;
                        best_idx = i;
                    }
                }
            }
            
            if (!found_matching_quotient) {
				if (y == 1) {
					for (int i = 0; i < n; i++) {
						int remainder = values[i] % 13;
						if (remainder > best_remainder) {
							best_remainder = remainder;
							best_idx = i;
						}
					}
				} else{
                    int found_non_three = 0;
                    for (int i = 0; i < n; i++) {
						int remainder = values[i] % 13;
                        if (values[i] / 13 != 3 && remainder > best_remainder) {
                            best_remainder = remainder;
                            best_idx = i;
                            found_non_three = 1;
                        }
                    }
                    
                    if (!found_non_three) {
                        for (int i = 0; i < n; i++) {
							int remainder = values[i] % 13;
                            if (remainder > best_remainder) {
                                best_remainder = remainder;
                                best_idx = i;
                            }
                        }
                    }
				}
            }
        }
    }
    
    return ptr_array[best_idx];
}