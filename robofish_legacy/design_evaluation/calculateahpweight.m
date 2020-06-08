% Input convention:
%   A B C
% A 1 2 1
% B 0 1 0.5
% C 0 0 1
% 
% A is twice as important than B and equally important to C.
% B is half as important than C.
% input = [1 2 1; 0 1 0.5; 0 0 1]
% weight = [0.4; 0.2; 0.4]

function weight = calculateahpweight(input)
    ahp = constructAhp(input);
    weight = calculateWeight(ahp);
end

function weight = calculateWeight (ahp)
    weight = sum(ahp, 2) / sum(sum(ahp, 2));
end

function ahp = constructAhp (input)
    ahp = input + tril(1 ./ transpose(input)) - eye(size(input));
    ahp = ahp ./ sum(ahp, 1);
end