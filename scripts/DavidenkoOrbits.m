v = VideoWriter('Davidenko', 'Motion JPEG AVI');
v.FrameRate = 24;
v.Quality = 100;
open(v);
timesteps = size(Tsteps, 2);
%TheMovie(timesteps) = struct('cdata', [], 'colormap', []);
figure();
for i=1:timesteps
    scatter(Positions(:, i), repmat(Tsteps(1, i), 1000, 1), 30, Positions(:, 1))
    ylim([0, 3]);
    hold on
    xlabel('Positions'); ylabel('Time');
    frame = getframe(gcf);
    writeVideo(v, frame);
end
hold off
close(v);