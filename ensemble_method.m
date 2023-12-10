
u = [[0 -0.1 0.025 0.15 0.2 0.29 0.37 0.3 0 ]];
z = [[0 -5 18 40 50 66 85 50 8]];

M1 = 0;
M2 = 1;
R =   1;
t = 0.8;

i =4;
phi_uu = zeros(M2 - M1 + 1, M2 - M1 + 1);

for k = 0:M2-M1
    
    for j = 0:M2-M1
        phi_uu(k+1,j+1) = phi_uu_ijk(i, k+M1,j+M1, R, u); 
    end

end

phi_zu = zeros(M2-M1+1,1);

for k = 0:M2-M1
    phi_zu(k+1) = phi_zu_ik(i,k+M1,R,u,z); 
end

h = phi_uu\phi_zu/t;

function result_z = phi_zu_ik(i, k, R, u,z)
    result_z = 0;
    
    for r = 1:R
        % Adjust indices to handle negative values
        index_k = i - k;
        
        % Set the value to zero if the index is negative
        if i < 1
            z_i = 0;
        else
            z_i = z(r, i);
        end
        
        if index_k < 1
            u_k = 0;
        else
            u_k = u(r, index_k);
        end
        
        result_z = result_z + z_i * u_k;
    end
    
    result_z = result_z / R;
end

function result = phi_uu_ijk(i, j, k, R, u)
    result = 0;
    
    for r = 1:R
        % Adjust indices to handle negative values
        index_i = i - j;
        index_k = i - k;
        
        % Set the value to zero if the index is negative
        if index_i < 1
            u_i = 0;
        else
            u_i = u(r, index_i);
        end
        
        if index_k < 1
            u_k = 0;
        else
            u_k = u(r, index_k);
        end
        
        result = result + u_i * u_k;
    end
    
    result = result / R;
end



