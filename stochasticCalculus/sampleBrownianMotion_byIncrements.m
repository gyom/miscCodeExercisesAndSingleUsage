function X = sampleBrownianMotion_byIncrements(domain, nPaths)
    % domain = [linspace(0,1,10, linspace(1, 5, 10)]
    % nPaths = 10

    if nargin < 2
        nPaths = 1;
    end
    
    N = numel(domain);
    X = zeros(nPaths, N);
    
    if N <= 1 || nPaths < 1
        return;
    end
    
    timeDifferences = toRow(domain(2:end) - domain(1:end-1));
    if any(timeDifferences < 0)
        fprintf('The times provided are not ordered.\n');
        fprintf('We will automatically order them, but if you match the output with those times, you might get wrong results.\n');
        domain = sort(domain);
        timeDifferences = toRow(domain(2:end) - domain(1:end-1));
    end
    
    % scaling in this manner even takes care of the 0 time increments
    dBt = repmat(sqrt(timeDifferences), [nPaths,1]).*randn(nPaths, N-1);
    
    X(:, 2:end) = cumsum(dBt,2);
    
end

%%%
%
%   nPaths = 10;
%   X = sampleBrownianMotion_byIncrements(linspace(0,1, 20), nPaths);
%   
%   colormap = lines;
%   figure, hold on;
%   for p=1:nPaths
%       plot(X(p,:), 'Color', colormap(rem(p, size(colormap,1)),:), 'LineWidth', 1)
%   end
%
%%%

