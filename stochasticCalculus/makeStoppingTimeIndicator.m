function f = makeStoppingTimeIndicator(lowerBound, upperBound)
    % vectorial, but ignores time t
    function v = g(t, Bt)
        [nPaths, L] = size(Bt);
        %v = ones(size(Bt));
        v = Bt;
        %size(t)
        %size(Bt)
        assert(all(size(t) == size(Bt)));
        for r=1:nPaths
            stoppingTime = find((Bt(r,:) <= lowerBound) | (upperBound <= Bt(r,:)), 1, 'first');
            if ~isempty(stoppingTime)
                % whether it's an upper or lower bound, clamp that value
                if Bt(r,stoppingTime) <= lowerBound
                    v(r,stoppingTime:end) = lowerBound;
                elseif Bt(r,stoppingTime) >= upperBound
                    v(r,stoppingTime:end) = upperBound;
                end
            end
        end
    end

    f = @g;
end