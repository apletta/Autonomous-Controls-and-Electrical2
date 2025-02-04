% Returns individual rows/cols of the given matrix. 
% e.g. takes in a 2 rowed matrix of points and returns x and y coordinates
function varargout = points2xy(mat)

s = size(mat);

% Determines shape of matrix
if s(1) < s(2)
    for i = 1:length(mat(:,1))
        varargout{i} = mat(i,:);
    end
else
    for i = 1:length(mat(1,:))
        varargout{i} = mat(:,i);
    end
end