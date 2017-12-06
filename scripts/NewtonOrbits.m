its = size(Positions, 1);
for i=1:(its -1)
    scatter3(Positions(i+1, :), i*ones(1,100), Positions(i, :), 30, Positions(1, :));
    hold on
    xlabel('Position'); ylabel('Iteration'); zlabel('Past Position');
    yticks([1, 2, 3]);
end
hold off

